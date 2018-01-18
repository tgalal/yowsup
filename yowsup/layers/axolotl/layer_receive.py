from .layer_base import AxolotlBaseLayer

from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

from axolotl.util.hexutil import HexUtil
from axolotl.util.keyhelper import KeyHelper
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
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
from axolotl.ecc.curve import Curve

import binascii
import logging
import copy
import sys
logger = logging.getLogger(__name__)

class AxolotlReceivelayer(AxolotlBaseLayer):
    _COUNT_PREKEYS = 200

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
            elif protocolTreeNode.tag == "notification": #and protocolTreeNode["type"] == "encrypt":
                self.onEncryptNotification(protocolTreeNode)
                return
            elif not protocolTreeNode.tag == "receipt":
                #receipts will be handled by send layer
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
    def onEncryptNotification(self, protocolTreeNode):
        entity = EncryptNotification.fromProtocolTreeNode(protocolTreeNode)
        ack = OutgoingAckProtocolEntity(protocolTreeNode["id"], "notification", protocolTreeNode["type"], protocolTreeNode["from"])
        self.toLower(ack.toProtocolTreeNode())
        self.sendKeys(fresh=False, countPreKeys = self.__class__._COUNT_PREKEYS - entity.getCount())

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
            logger.warning("InvalidMessage or InvalidKeyIdException for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))

            from yowsup.layers.axolotl.protocolentities.iq_key_get import GetKeysIqProtocolEntity
            logger.info("Trying GetKeys for %s, getting keys now", encMessageProtocolEntity.getAuthor(False))
            entity = GetKeysIqProtocolEntity([encMessageProtocolEntity.getAuthor(False)])

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
            if type(plaintext) == bytes:
                # DEBUG SET RECEIPT
                # self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"], 'read', participant=node["participant"]).toProtocolTreeNode())

                if plaintext[0:1] == b'\n':
                    msg = plaintext[3:3+plaintext[1:2][-1]]
                elif plaintext[2:3] == b'\x01':
                    msg = plaintext[5:5+plaintext[4:5][-1]]
                    if msg[0:1] == b'\x01':
                        msg = plaintext[6:6+plaintext[4:5][-1]]
                else:
                    msg = plaintext[4:4+plaintext[3:4][-1]]

                # self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)
                self.handleConversationMessage(node, msg.decode())
                # self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext.split(b'\x8a')[0])
                return

            try:
                padding = ord(plaintext[-1]) & 0xFF
                plaintext = plaintext[:-padding]
                plaintext = plaintext.encode() if sys.version_info >= (3, 0) else plaintext
                self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)
            except Exception as ex: #(AttributeError, TypeError)
                logger.error('Exception')
                logger.error('Exception %s' % ex)



        except NoSessionException as e:
            logger.warning("No session for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node, self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())

    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        node = encMessageProtocolEntity.toProtocolTreeNode()
        m = Message()
        try:
            if sys.version_info >= (3,0) and isinstance(serializedData, str):
                serializedData = serializedData.encode()
        except AttributeError:
            logger.warning("AttributeError: 'bytes' object has no attribute 'encode'. Skipping 'encode()'")
            pass
        handled = False
        try:
            m.ParseFromString(serializedData)
        except:
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
        elif m.HasField("video_message"):
            handled = True
            self.handleVideoMessage(node, m.video_message)
        elif m.HasField("audio_message"):
            self.handleAudioMessage(node, m.audio_message)
        elif m.HasField("document_message"):
            handled = True
            self.handleDocumentMessage(node, m.document_message)
        elif not handled:
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
            "mediakey": imageMessage.media_key,
            "caption": imageMessage.caption,
            "encoding": "raw",
            "file": "enc",
            "ip": "0"
        }, data = imageMessage.jpeg_thumbnail)
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

    # TODO: Create own URLNode
    def handleUrlMessage(self, originalEncNode, urlMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "text"
        messageNode.children = []
        messageNode.addChild(ProtocolTreeNode("body", data = urlMessage.text))
        self.toUpper(messageNode)

    def handleDocumentMessage(self, originalEncNode, documentMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "document",
            "title": documentMessage.title,
            "filehash": documentMessage.file_sha256,
            "size": str(documentMessage.file_length),
            "url": documentMessage.url,
            "mimetype": documentMessage.mime_type.split(';')[0],
            "pagecount": str(documentMessage.page_count),
            "mediakey": documentMessage.media_key
        })
        messageNode.addChild(mediaNode)
        self.toUpper(messageNode)


    def handleLocationMessage(self, originalEncNode, locationMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "latitude": locationMessage.degrees_latitude,
            "longitude": locationMessage.degrees_longitude,
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


    ### keys set and get
    def sendKeys(self, fresh=True, countPreKeys=_COUNT_PREKEYS):
        identityKeyPair = KeyHelper.generateIdentityKeyPair() if fresh else self.store.getIdentityKeyPair()
        registrationId = KeyHelper.generateRegistrationId() if fresh else self.store.getLocalRegistrationId()
        preKeys = KeyHelper.generatePreKeys(KeyHelper.getRandomSequence(), countPreKeys)
        signedPreKey = KeyHelper.generateSignedPreKey(identityKeyPair, KeyHelper.getRandomSequence(65536))
        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))

        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]),
                                            signedKeyTuple, preKeysDict, Curve.DJB_TYPE, self.adjustId(registrationId))

        onResult = lambda _, __: self.persistKeys(registrationId, identityKeyPair, preKeys, signedPreKey, fresh)
        self._sendIq(setKeysIq, onResult) # TODO: reintroduce error handler (was _sendIq(setKeysIq, onResult, self.onSentKeysError))

    def persistKeys(self, registrationId, identityKeyPair, preKeys, signedPreKey, fresh):
        total = len(preKeys)
        curr = 0
        prevPercentage = 0

    def adjustArray(self, arr):
        return HexUtil.decodeHex(binascii.hexlify(arr))

    def adjustId(self, _id):
        _id = format(_id, 'x')
        zfiller = len(_id) if len(_id) % 2 == 0 else len(_id) + 1
        _id = _id.zfill(zfiller if zfiller > 6 else 6)
        return binascii.unhexlify(_id)
