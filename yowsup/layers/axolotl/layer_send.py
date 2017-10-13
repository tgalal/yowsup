from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.protocol_messages.proto.wa_pb2 import SenderKeyDistributionMessage as ProtoSenderKeyDistributionMessage
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_groups.protocolentities import InfoGroupsIqProtocolEntity, InfoGroupsResultIqProtocolEntity
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.axolotladdress import AxolotlAddress
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from yowsup.common.tools                               import Jid
import binascii

import logging
from random import randint

from .layer_base import AxolotlBaseLayer

logger = logging.getLogger(__name__)

class AxolotlSendLayer(AxolotlBaseLayer):
    MAX_SENT_QUEUE = 100
    def __init__(self):
        super(AxolotlSendLayer, self).__init__()

        self.sessionCiphers = {}
        self.groupSessionBuilder = None
        self.groupCiphers = {}
        '''
            Sent messages will be put in skalti entQueue until we receive a receipt for them.
            This is for handling retry receipts which requires re-encrypting and resend of the original message
            As the receipt for a sent message might arrive at a different yowsup instance,
            ideally the original message should be fetched from a persistent storage.
            Therefore, if the original message is not in sentQueue for any reason, we will
            notify the upper layers and let them handle it.
        '''
        self.sentQueue = []

    def onNewStoreSet(self, store):
        if store is not None:
            self.groupSessionBuilder = GroupSessionBuilder(store)

    def __str__(self):
        return "Axolotl Layer"

    def handleEncNode(self, node):
        recipient_id = node["to"].split('@')[0]
        v2 = node["to"]
        if node.getChild("enc"):  # media enc is only for v2 messsages
            if '-' in recipient_id: ## Handle Groups
                def getResultNodes(resultNode, requestEntity):
                    groupInfo = InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(resultNode)
                    jids = list(groupInfo.getParticipants().keys()) #keys in py3 returns dict_keys
                    jids.remove(self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(True))
                    jidsNoSession = []
                    for jid in jids:
                        if not self.store.containsSession(jid.split('@')[0], 1):
                            jidsNoSession.append(jid)
                    if len(jidsNoSession):
                        self.getKeysFor(jidsNoSession, lambda successJids, b: self.sendToGroupWithSessions(node, successJids))
                    else:
                        self.sendToGroupWithSessions(node, jids)

                groupInfoIq = InfoGroupsIqProtocolEntity(Jid.normalize(node["to"]))
                self._sendIq(groupInfoIq, getResultNodes)
            else:
                messageData = self.serializeToProtobuf(node)
                # print (messageData)
                if not self.store.containsSession(recipient_id, 1):
                    self.getKeysFor([node["to"]], lambda successJids, b: self.sendToContact(node) if len(successJids) == 1 else self.toLower(node), lambda: self.toLower(node))
                if messageData:
                    sessionCipher = self.getSessionCipher(recipient_id)
                    messageData = messageData.SerializeToString() + self.getPadding()
                    ciphertext = sessionCipher.encrypt(messageData)
                    mediaType = node.getChild("enc")["type"] if node.getChild("enc") else None

                    encEntity = EncryptedMessageProtocolEntity(
                        [
                            EncProtocolEntity(
                                EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG,
                                2 if v2 else 1,
                                ciphertext.serialize(), mediaType)],
                        "text" if not mediaType else "media",
                        _id=node["id"],
                        to=node["to"],
                        notify=node["notify"],
                        timestamp=node["timestamp"],
                        participant=node["participant"],
                        offline=node["offline"],
                        retry=node["retry"]
                    )
                    self.toLower(encEntity.toProtocolTreeNode())
                else:  # case of unserializable messages (audio, video) ?
                    self.toLower(node)
        else:
            self.toLower(node)

    def send(self, node):
        # if node.tag == "message" and node["to"] not in self.skipEncJids and not node.getChild("enc") or (node.getChild("media") and node.getChild("media")["mediakey"]):
        if node.tag == "message" and node["to"] not in self.skipEncJids and not node.getChild("enc"):
            self.processPlaintextNodeAndSend(node)
        # elif node.tag == "iq" and node["xmlns"] == "w:m":
        #     mediaNode = node.getChild("media")
        #     if mediaNode and mediaNode["type"] == "image":
        #         iqNode = IqProtocolEntity.fromProtocolTreeNode(node).toProtocolTreeNode()
        #         iqNode.addChild(ProtocolTreeNode(
        #             "encr_media", {
        #                 "type": mediaNode["type"],
        #                 "hash": mediaNode["hash"]
        #             }
        #         ))
        #         self.toLower(iqNode)
        elif node.getChild("enc"):
            self.handleEncNode(node)
        else:
            self.toLower(node)

    def receive(self, protocolTreeNode):
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "receipt":
                '''
                Going to keep all group message enqueued, as we get receipts from each participant
                So can't just remove it on first receipt. Therefore, the MAX queue length mechanism should better be working
                '''
                messageNode = self.getEnqueuedMessageNode(protocolTreeNode["id"], protocolTreeNode["participant"] is not None)
                if not messageNode:
                    logger.debug("Axolotl layer does not have the message, bubbling it upwards")
                    self.toUpper(protocolTreeNode)
                elif protocolTreeNode["type"] == "retry":
                    logger.info("Got retry to for message %s, and Axolotl layer has the message" % protocolTreeNode["id"])
                    retryReceiptEntity = RetryIncomingReceiptProtocolEntity.fromProtocolTreeNode(protocolTreeNode)
                    self.toLower(retryReceiptEntity.ack().toProtocolTreeNode())
                    self.getKeysFor(
                        [protocolTreeNode["participant"] or protocolTreeNode["from"]],
                        lambda successJids, b: self.processPlaintextNodeAndSend(messageNode, retryReceiptEntity) if len(successJids) == 1 else None
                    )
                else:
                    #not interested in any non retry receipts, bubble upwards
                    self.toUpper(protocolTreeNode)

    def processPlaintextNodeAndSend(self, node, retryReceiptEntity = None):
        recipient_id = node["to"].split('@')[0]
        isGroup = "-" in recipient_id

        if isGroup:
            self.sendToGroup(node, retryReceiptEntity)
        elif self.store.containsSession(recipient_id, 1):
            self.sendToContact(node)
        else:
            self.getKeysFor([node["to"]], lambda successJids, b: self.sendToContact(node) if len(successJids) == 1 else self.toLower(node), lambda: self.toLower(node))



    def getPadding(self):
        num = randint(1,255)
        return bytearray([num] * num)

    def groupSendSequence(self):
        """
        check if senderkeyrecord exists
            no: - create,
                - get group jids from info request
                - for each jid without a session, get keys to create the session
                - send message with dist key for all participants
            yes:
                - send skmsg without any dist key

        received retry for a participant
            - request participants keys
            - send message with dist key only + conversation, only for this participat
        :return:
        """

    def enqueueSent(self, node):
        if len(self.sentQueue) >= self.__class__.MAX_SENT_QUEUE:
            logger.warn("Discarding queued node without receipt")
            self.sentQueue.pop(0)
        self.sentQueue.append(node)

    def getEnqueuedMessageNode(self, messageId, keepEnqueued = False):
        for i in range(0, len(self.sentQueue)):
            if self.sentQueue[i]["id"] == messageId:
                if keepEnqueued:
                    return self.sentQueue[i]
                return self.sentQueue.pop(i)


    def sendEncEntities(self, node, encEntities):
        mediaType = None
        messageEntity = EncryptedMessageProtocolEntity(encEntities,
                                           "text" if not mediaType else "media",
                                           _id=node["id"],
                                           to=node["to"],
                                           notify=node["notify"],
                                           timestamp=node["timestamp"],
                                           participant=node["participant"],
                                           offline=node["offline"],
                                           retry=node["retry"]
                                           )
        self.enqueueSent(node)
        self.toLower(messageEntity.toProtocolTreeNode())

    def sendToContact(self, node):
        recipient_id = node["to"].split('@')[0]
        cipher = self.getSessionCipher(recipient_id)
        messageData = self.serializeToProtobuf(node).SerializeToString() + self.getPadding()

        ciphertext = cipher.encrypt(messageData)
        mediaType = node.getChild("media")["type"] if node.getChild("media") else None

        return self.sendEncEntities(node, [EncProtocolEntity(EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG, 2, ciphertext.serialize(), mediaType)])

    def sendToGroupWithSessions(self, node, jidsNeedSenderKey = None, retryCount=0):
        jidsNeedSenderKey = jidsNeedSenderKey or []
        groupJid = node["to"]
        ownNumber = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(False)
        senderKeyName = SenderKeyName(groupJid, AxolotlAddress(ownNumber, 0))
        cipher = self.getGroupCipher(groupJid, ownNumber)
        encEntities = []
        if len(jidsNeedSenderKey):
            senderKeyDistributionMessage = self.groupSessionBuilder.create(senderKeyName)
            for jid in jidsNeedSenderKey:
                sessionCipher = self.getSessionCipher(jid.split('@')[0])
                message =  self.serializeSenderKeyDistributionMessageToProtobuf(node["to"], senderKeyDistributionMessage)

                if retryCount > 0:
                    message = self.serializeToProtobuf(node, message)

                ciphertext = sessionCipher.encrypt(message.SerializeToString() + self.getPadding())
                encEntities.append(
                    EncProtocolEntity(
                            EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG
                        , 2, ciphertext.serialize(), jid=jid
                    )
                )

        if not retryCount:
            messageData = self.serializeToProtobuf(node).SerializeToString()
            ciphertext = cipher.encrypt(messageData + self.getPadding())
            mediaType = node.getChild("media")["type"] if node.getChild("media") else None

            encEntities.append(EncProtocolEntity(EncProtocolEntity.TYPE_SKMSG, 2, ciphertext, mediaType))

        self.sendEncEntities(node, encEntities)

    def ensureSessionsAndSendToGroup(self, node, jids):
        jidsNoSession = []
        for jid in jids:
            if not self.store.containsSession(jid.split('@')[0], 1):
                jidsNoSession.append(jid)

        if len(jidsNoSession):
            self.getKeysFor(jidsNoSession, lambda successJids, b: self.sendToGroupWithSessions(node, successJids))
        else:
            self.sendToGroupWithSessions(node, jids)

    def sendToGroup(self, node, retryReceiptEntity = None):
        groupJid = node["to"]
        ownNumber = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(False)
        ownJid = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(True)
        senderKeyName = SenderKeyName(node["to"], AxolotlAddress(ownNumber, 0))
        senderKeyRecord = self.store.loadSenderKey(senderKeyName)


        def sendToGroup(resultNode, requestEntity):
            groupInfo = InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(resultNode)
            jids = list(groupInfo.getParticipants().keys()) #keys in py3 returns dict_keys
            jids.remove(ownJid)
            return self.ensureSessionsAndSendToGroup(node, jids)

        if senderKeyRecord.isEmpty():
            groupInfoIq = InfoGroupsIqProtocolEntity(groupJid)
            self._sendIq(groupInfoIq, sendToGroup)
        else:
            retryCount = 0
            jidsNeedSenderKey = []
            if retryReceiptEntity is not None:
                retryCount = retryReceiptEntity.getRetryCount()
                jidsNeedSenderKey.append(retryReceiptEntity.getRetryJid())
            self.sendToGroupWithSessions(node, jidsNeedSenderKey, retryCount)

    def serializeToProtobuf(self, node, message = None):
        if node.getChild("body"):
            return self.serializeTextToProtobuf(node, message)
        elif node.getChild("enc"):
            return self.serializeMediaToProtobuf(node.getChild("enc"), message)
        else:
            raise ValueError("No body or media nodes found")

    def serializeTextToProtobuf(self, node, message = None):
        m = message or Message()
        m.conversation = node.getChild("body").getData()
        return m

    def serializeMediaToProtobuf(self, mediaNode, message = None):
        if mediaNode["type"] == "image":
            return self.serializeImageToProtobuf(mediaNode, message)
        if mediaNode["type"] == "location":
            return self.serializeLocationToProtobuf(mediaNode, message)
        if mediaNode["type"] == "vcard":
            return self.serializeContactToProtobuf(mediaNode, message)

        return None

    def serializeLocationToProtobuf(self, mediaNode, message = None):
        m = message or Message()
        location_message = LocationMessage()
        location_message.degrees_latitude = float(mediaNode["latitude"])
        location_message.degrees_longitude = float(mediaNode["longitude"])
        location_message.address = mediaNode["name"]
        location_message.name = mediaNode["name"]
        location_message.url = mediaNode["url"]

        location_message.jpeg_thumbnail = b''
        m.location_message.MergeFrom(location_message)

        return m

    def serializeContactToProtobuf(self, mediaNode, message = None):
        vcardNode = mediaNode.getChild("vcard")
        m = message or Message()
        contact_message = ContactMessage()
        contact_message.display_name = vcardNode["name"]
        m.vcard = vcardNode.getData()
        m.contact_message.MergeFrom(contact_message)

        return m

    def serializeImageToProtobuf(self, mediaNode, message = None):
        m = message or Message()
        image_message = ImageMessage()
        image_message.url = mediaNode["url"]
        image_message.width = int(mediaNode["width"])
        image_message.height = int(mediaNode["height"])
        image_message.mime_type = mediaNode["mimetype"]
        image_message.media_key = mediaNode["mediakey"]
        image_message.file_sha256 = binascii.unhexlify(mediaNode["filehash"].encode())
        image_message.file_length = int(mediaNode["size"])
        image_message.media_key = binascii.unhexlify(mediaNode["anu"])
        image_message.file_enc_sha256 = binascii.unhexlify(mediaNode["file_enc_sha256"])
        image_message.caption = mediaNode["caption"] or ""
        image_message.jpeg_thumbnail = mediaNode.getData()

        m.image_message.MergeFrom(image_message)

        return m

    def serializeUrlToProtobuf(self, node, message = None):
        pass

    def serializeDocumentToProtobuf(self, node, message = None):
        pass

    def serializeSenderKeyDistributionMessageToProtobuf(self, groupId, senderKeyDistributionMessage, message = None):
        m = message or Message()
        sender_key_distribution_message = ProtoSenderKeyDistributionMessage()
        sender_key_distribution_message.groupId = groupId
        sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        m.sender_key_distribution_message.MergeFrom(sender_key_distribution_message)
        # m.conversation = text
        return m
    ###

    def getSessionCipher(self, recipientId):
        if recipientId in self.sessionCiphers:
            sessionCipher = self.sessionCiphers[recipientId]
        else:
            sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            self.sessionCiphers[recipientId] = sessionCipher

        return sessionCipher

    def getGroupCipher(self, groupId, senderId):
        senderKeyName = SenderKeyName(groupId, AxolotlAddress(senderId, 0))
        if senderKeyName in self.groupCiphers:
            groupCipher = self.groupCiphers[senderKeyName]
        else:
            groupCipher = GroupCipher(self.store, senderKeyName)
            self.groupCiphers[senderKeyName] = groupCipher
        return groupCipher
