import json

from .layer_base import AxolotlBaseLayer

from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

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
    def __init__(self):
        super(AxolotlReceivelayer, self).__init__()
        self.v2Jids = [] #people we're going to send v2 enc messages
        self.sessionCiphers = {}
        self.groupCiphers = {}
        self.pendingIncomingMessages = {} #(jid, participantJid?) => message

    def receive(self, protocolTreeNode):
        """
        :type protocolTreeNode: ProtocolTreeNode
        """
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "message":
                self.onMessage(protocolTreeNode)
            elif not protocolTreeNode.tag == "receipt":
                # receipts will be handled by send layer
                self.toUpper(protocolTreeNode)

            # elif protocolTreeNode.tag == "iq":
            #     if protocolTreeNode.getChild("encr_media"):
            #         protocolTreeNode.addChild("media", {
            #             "url": protocolTreeNode["url"],
            #             "ip": protocolTreeNode["ip"],
            #         })
            #         self.toUpper(protocolTreeNode)
            #         return

    ######

    def onEncrMediaResult(self, resultNode):
        pass


    def processPendingIncomingMessages(self, jid, participantJid = None):
        conversationIdentifier = (jid, participantJid)
        if conversationIdentifier in self.pendingIncomingMessages:
            for messageNode in self.pendingIncomingMessages[conversationIdentifier]:
                self.onMessage(messageNode)

            del self.pendingIncomingMessages[conversationIdentifier]

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
        if node.getChild("enc")["v"] == "2" and node["from"] not in self.v2Jids:
            self.v2Jids.append(node["from"])
        try:
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG):
                self.handlePreKeyWhisperMessage(node)
            elif encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG):
                self.handleWhisperMessage(node)
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG):
                self.handleSenderKeyMessage(node)
        except (InvalidMessageException, InvalidKeyIdException) as e:
            logger.warning("InvalidMessage or KeyId for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node, self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except NoSessionException as e:
            logger.warning("No session for %s, getting their keys now", encMessageProtocolEntity.getAuthor(False))

            conversationIdentifier = (node["from"], node["participant"])

            if conversationIdentifier not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[conversationIdentifier] = []
            self.pendingIncomingMessages[conversationIdentifier].append(node)

            successFn = lambda successJids, b: self.processPendingIncomingMessages(*conversationIdentifier) if len(successJids) else None

            self.getKeysFor([senderJid], successFn)

        except DuplicateMessageException as e:
            logger.warning("Received a message that we've previously decrypted, goint to send the delivery receipt myself")
            self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"], participant=node["participant"]).toProtocolTreeNode())

        except UntrustedIdentityException as e:
            if self.getProp(PROP_IDENTITY_AUTOTRUST, False):
                logger.warning("Autotrusting identity for %s", e.getName())
                self.store.saveIdentity(e.getName(), e.getIdentityKey())
                return self.handleEncMessage(node)
            else:
                logger.error("Ignoring message with untrusted identity")

    def handlePreKeyWhisperMessage(self, node):
        pkMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = pkMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG)
        preKeyWhisperMessage = PreKeyWhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(pkMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptPkmsg(preKeyWhisperMessage)
        if enc.getVersion() == 2:
            paddingByte = plaintext[-1] if type(plaintext[-1]) is int else ord(plaintext[-1])
            padding = paddingByte & 0xFF
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
            paddingByte = plaintext[-1] if type(plaintext[-1]) is int else ord(plaintext[-1])
            padding = paddingByte & 0xFF
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
            plaintext = plaintext[:-padding]
            plaintext = plaintext.encode() if sys.version_info >= (3, 0) else plaintext
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)

        except NoSessionException as e:
            logger.warning("No session for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node, self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())

    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        node = encMessageProtocolEntity.toProtocolTreeNode()
        m = Message()
        handled = False
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
            handled = True
            axolotlAddress = AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 0)
            self.handleSenderKeyDistributionMessage(m.sender_key_distribution_message, axolotlAddress)

        if m.HasField("conversation"):
            handled = True
            self.handleConversationMessage(node, m.conversation)
        elif m.HasField("contact_message"):
            handled = True
            self.handleContactMessage(node, m.contact_message)
        elif m.HasField("url_message"):
            handled = True
            self.handleUrlMessage(node, m.url_message)
        elif m.HasField("location_message"):
            handled = True
            self.handleLocationMessage(node, m.location_message)
        elif m.HasField("image_message"):
            handled = True
            self.handleImageMessage(node, m.image_message)
        elif m.HasField("document_message"):
            handled = True
            self.handleDocumentMessage(node, m.document_message)
        elif m.HasField("video_message"):
            handled = True
            self.handleVideoMessage(node, m.video_message)
        elif m.HasField("audio_message"):
            handled = True
            self.handleAudioMessage(node, m.audio_message)
        if not handled:
            print(m.ListFields())
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
            "mediakey": imageMessage.media_key,
            "encoding": "raw",
            "file": "enc",
            "ip": "0"
        }, data = imageMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleAudioMessage(self, originalEncNode, audioMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "audio",
            "filehash": audioMessage.file_sha256,
            "size": str(audioMessage.file_length),
            "url": audioMessage.url,
            "mimetype": audioMessage.mime_type.split(';')[0],
            "encoding": audioMessage.mime_type.split(';')[1].strip() if len(audioMessage.mime_type.split(';')) > 1 else "",
            "duration": str(audioMessage.duration),
            "seconds": str(audioMessage.duration),
            "encoding": "raw",
            "file": "enc",
            "ip": "0",
            "mediakey": audioMessage.media_key
        })
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleVideoMessage(self, originalEncNode, videoMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "video",
            "filehash": videoMessage.file_sha256,
            "size": str(videoMessage.file_length),
            "url": videoMessage.url,
            "mimetype": videoMessage.mime_type.split(';')[0],
            "encoding": videoMessage.mime_type.split(';')[1].strip() if len(videoMessage.mime_type.split(';')) > 1 else "",
            "duration": str(videoMessage.duration),
            "seconds": str(videoMessage.duration),
            "caption": videoMessage.caption,
            "encoding": "raw",
            "file": "enc",
            "ip": "0",
            "mediakey": videoMessage.media_key
        }, data = videoMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleUrlMessage(self, originalEncNode, urlMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "url",
            "text": urlMessage.text,
            "match": urlMessage.matched_text,
            "url": urlMessage.canonical_url,
            "description": urlMessage.description,
            "title": urlMessage.title
        }, data = urlMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleDocumentMessage(self, originalEncNode, documentMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "document",
            "url": documentMessage.url,
            "mimetype": documentMessage.mime_type,
            "title": documentMessage.title,
            "filehash": documentMessage.file_sha256,
            "size": str(documentMessage.file_length),
            "pages": str(documentMessage.page_count),
            "mediakey": documentMessage.media_key
        }, data = documentMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleLocationMessage(self, originalEncNode, locationMessage):
        messageNode = copy.deepcopy(originalEncNode)
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
        messageNode = copy.deepcopy(originalEncNode)
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