from .layer_base import AxolotlBaseLayer

from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode

from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.invalidmessageexception import InvalidMessageException
from axolotl.duplicatemessagexception import DuplicateMessageException
from axolotl.invalidkeyidexception import InvalidKeyIdException
from axolotl.nosessionexception import NoSessionException
from axolotl.untrustedidentityexception import UntrustedIdentityException
from axolotl.axolotladdress import AxolotlAddress
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from axolotl.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage

import logging
import copy
logger = logging.getLogger(__name__)

class AxolotlReceivelayer(AxolotlBaseLayer):
    PROP_IDENTITY_AUTOTRUST =  "org.openwhatsapp.yowsup.prop.axolotl.INDENTITY_AUTOTRUST"
    def __init__(self):
        super(AxolotlReceivelayer, self).__init__()
        self.v2Jids = [] #people we're going to send v2 enc messages
        self.sessionCiphers = {}
        self.groupCiphers = {}
        self.pendingIncomingMessages = {}

    def receive(self, protocolTreeNode):
        """
        :type protocolTreeNode: ProtocolTreeNode
        """
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "message":
                self.onMessage(protocolTreeNode)
                return
            elif protocolTreeNode.tag == "receipt" and protocolTreeNode["type"] == "retry":
                # should bring up that message, resend it, but in upper layer?
                # as it might have to be fetched from a persistent storage
                pass
            self.toUpper(protocolTreeNode)


    def processPendingIncomingMessages(self, jid):
        if jid in self.pendingIncomingMessages:
            for messageNode in self.pendingIncomingMessages[jid]:
                self.onMessage(messageNode)

            del self.pendingIncomingMessages[jid]

    ##### handling received data #####

    def onMessage(self, protocolTreeNode):
        encNode = protocolTreeNode.getChild("enc")
        if encNode:
            self.handleEncMessage(protocolTreeNode)
        else:
            self.toUpper(protocolTreeNode)

    def handleEncMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        isGroup =  node["participant"] is not None
        senderJid = node["participant"] if isGroup else node["from"]
        encNode = None
        if node.getChild("enc")["v"] == "2" and senderJid not in self.v2Jids:
            self.v2Jids.append(senderJid)
        try:
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG):
                self.handlePreKeyWhisperMessage(node)
            elif encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG):
                self.handleWhisperMessage(node)
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG):
                self.handleSenderKeyMessage(node)
        except InvalidMessageException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except InvalidKeyIdException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except NoSessionException as e:
            logger.error(e)
            entity = GetKeysIqProtocolEntity([senderJid])
            if senderJid not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[senderJid] = []
            self.pendingIncomingMessages[senderJid].append(node)

            self._sendIq(entity, lambda a, b: self.onGetKeysResult(a, b, self.processPendingIncomingMessages), self.onGetKeysError)
        except DuplicateMessageException as e:
            logger.error(e)
            logger.warning("Going to send the delivery receipt myself !")
            self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"]).toProtocolTreeNode())

        except UntrustedIdentityException as e:
            if(self.getProp(self.__class__.PROP_IDENTITY_AUTOTRUST, False)):
                logger.warning("Autotrusting identity for %s" % e.getName())
                self.store.saveIdentity(e.getName(), e.getIdentityKey())
                return self.handleEncMessage(node)
            else:
                logger.error(e)
                logger.warning("Ignoring message with untrusted identity")
    def handlePreKeyWhisperMessage(self, node):
        pkMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = pkMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG)
        preKeyWhisperMessage = PreKeyWhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(pkMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptPkmsg(preKeyWhisperMessage)
        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(pkMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(node, plaintext)

    def handleWhisperMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)

        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG)
        whisperMessage = WhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(encMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptMsg(whisperMessage)

        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(encMessageProtocolEntity.toProtocolTreeNode(), plaintext)

    def handleSenderKeyMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG)

        senderKeyName = SenderKeyName(encMessageProtocolEntity.getFrom(True), AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 0))
        groupCipher = GroupCipher(self.store, senderKeyName)
        try:
            plaintext = groupCipher.decrypt(enc.getData())
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext[:-padding])
        except NoSessionException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())


    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        node = encMessageProtocolEntity.toProtocolTreeNode()
        m = Message()
        try:
            m.ParseFromString(serializedData)
        except:
            print("DUMP:")
            print(serializedData)
            print([s for s in serializedData])
            print([ord(s) for s in serializedData])
            raise
        if not m or not serializedData:
            raise ValueError("Empty message")

        if m.HasField("sender_key_distribution_message"):
            axolotlAddress = AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 0)
            self.handleSenderKeyDistributionMessage(m.sender_key_distribution_message, axolotlAddress)
        elif m.HasField("conversation"):
            self.handleConversationMessage(node, m.conversation)
        elif m.HasField("contact_message"):
            self.handleContactMessage(node, m.contact_message)
        elif m.HasField("url_message"):
            self.handleUrlMessage(node, m.url_message)
        elif m.HasField("location_message"):
            self.handleLocationMessage(node, m.location_message)
        elif m.HasField("image_message"):
            self.handleImageMessage(node, m.image_message)
        else:
            print(m)
            raise ValueError("Unhandled")

    def handleSenderKeyDistributionMessage(self, senderKeyDistributionMessage, axolotlAddress):
        groupId = senderKeyDistributionMessage.groupId
        axolotlSenderKeyDistributionMessage = SenderKeyDistributionMessage(serialized=senderKeyDistributionMessage.axolotl_sender_key_distribution_message)
        groupSessionBuilder = GroupSessionBuilder(self.store)
        senderKeyName = SenderKeyName(groupId, axolotlAddress)
        groupSessionBuilder.process(senderKeyName, axolotlSenderKeyDistributionMessage)

    def handleConversationMessage(self, originalEncNode, text):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode.children = []
        messageNode.addChild(ProtocolTreeNode("body", data = text))
        self.toUpper(messageNode)

    def handleImageMessage(self, originalEncNode, imageMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "image",
            "filehash": imageMessage.file_sha256,
            "size": str(imageMessage.file_length),
            "url": imageMessage.url,
            "mimetype": imageMessage.mime_type,
            "width": imageMessage.width,
            "height": imageMessage.height,
            "caption": imageMessage.caption,
            "encoding": "raw",
            "file": "enc",
            "ip": "0"
        }, data = imageMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleUrlMessage(self, originalEncNode, urlMessage):
        #convert to ??
        pass

    def handleDocumentMessage(self, originalEncNode, documentMessage):
        #convert to ??
        pass

    def handleLocationMessage(self, originalEncNode, locationMessage):
        messageNode = copy.deepycopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "latitude": locationMessage.degrees_latitude,
            "longitude": locationMessage.degress_longitude,
            "name": "%s %s" % (locationMessage.name, locationMessage.address),
            "url": locationMessage.url,
            "encoding": "raw",
            "type": "location"
        }, data=locationMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)
        self.toUpper(messageNode)

    def handleContactMessage(self, originalEncNode, contactMessage):
        messageNode = copy.deepycopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "vcard"
        }, [
            ProtocolTreeNode("vcard", {"name": contactMessage.display_name}, data = contactMessage.vcard)
        ] )
        messageNode.addChild(mediaNode)
        self.toUpper(messageNode)



    def getSessionCipher(self, recipientId):
        if recipientId in self.sessionCiphers:
            sessionCipher = self.sessionCiphers[recipientId]
        else:
            sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            self.sessionCiphers[recipientId] = sessionCipher

        return sessionCipher

    def getGroupCipher(self, groupId, senderId):
        senderKeyName = SenderKeyName(groupId, AxolotlAddress(senderId, 1))
        if senderKeyName in self.groupCiphers:
            groupCipher = self.groupCiphers[senderKeyName]
        else:
            groupCipher = GroupCipher(self.store, senderKeyName)
            self.groupCiphers[senderKeyName] = groupCipher
        return groupCipher
