from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_groups.protocolentities import InfoGroupsIqProtocolEntity, InfoGroupsResultIqProtocolEntity
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from yowsup.common.tools import Jid
from yowsup.layers.protocol_messages.protocolentities.message import MessageAttributes
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
        self.groupCiphers = {}
        '''
            Sent messages will be put in Queue until we receive a receipt for them.
            This is for handling retry receipts which requires re-encrypting and resend of the original message
            As the receipt for a sent message might arrive at a different yowsup instance,
            ideally the original message should be fetched from a persistent storage.
            Therefore, if the original message is not in sentQueue for any reason, we will
            notify the upper layers and let them handle it.
        '''
        self.sentQueue = []


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
                        if not self.manager.session_exists(jid.split('@')[0]):
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
                if messageData:
                    ciphertext = self.manager.encrypt(recipient_id, messageData)
                    mediaType = node.getChild("enc")["type"] if node.getChild("enc") else None

                    encEntity = EncryptedMessageProtocolEntity(
                        [
                            EncProtocolEntity(
                                EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG,
                                2 if v2 else 1,
                                ciphertext.serialize(), mediaType)],
                        "text" if not mediaType else "media",
                        MessageAttributes.from_message_protocoltreenode(node)
                    )
                    self.toLower(encEntity.toProtocolTreeNode())
                else:  # case of unserializable messages (audio, video) ?
                    self.toLower(node)
        else:
            self.toLower(node)

    def send(self, node):
        # if node.tag == "message" and node["to"] not in self.skipEncJids and not node.getChild("enc") or (node.getChild("media") and node.getChild("media")["mediakey"]):
        if node.tag == "message" and not node.getChild("enc") and (node["to"] not in self.skipEncJids or node.getChild("proto") is not None):
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
        elif self.manager.session_exists(recipient_id):
            self.sendToContact(node)
        else:
            self.getKeysFor([node["to"]], lambda successJids, b: self.sendToContact(node) if len(successJids) == 1 else self.toLower(node), lambda: self.toLower(node))

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
        logger.debug("enqueueSent(node=[omitted])")
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

    def sendEncEntities(self, node, encEntities, participant=None):
        logger.debug("sendEncEntities(node=[omitted], encEntities=[omitted], participant=%s)" % participant)
        message_attrs = MessageAttributes.from_message_protocoltreenode(node)
        message_attrs.participant = participant
        messageEntity = EncryptedMessageProtocolEntity(
            encEntities,
            node["type"],
            message_attrs
        )
        # if participant is set, this message is directed to that specific participant as a result of a retry, therefore
        # we already have the original group message and there is no need to store it again.
        if participant is None:
            self.enqueueSent(node)
        self.toLower(messageEntity.toProtocolTreeNode())

    def sendToContact(self, node):
        recipient_id = node["to"].split('@')[0]

        protoNode = node.getChild("proto")
        messageData = protoNode.getData()

        ciphertext = self.manager.encrypt(
            recipient_id,
            messageData
        )
        mediaType = protoNode["mediatype"]
        return self.sendEncEntities(node, [EncProtocolEntity(EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG, 2, ciphertext.serialize(), mediaType)])

    def sendToGroupWithSessions(self, node, jidsNeedSenderKey = None, retryCount=0):
        """
        For each jid in jidsNeedSenderKey will create a pkmsg enc node with the associated jid.
        If retryCount > 0 and we have only one jidsNeedSenderKey, this is a retry requested by a specific participant
        and this message is to be directed at specific at that participant indicated by jidsNeedSenderKey[0]. In this
        case the participant's jid would go in the parent's EncryptedMessage and not into the enc node.
        """
        logger.debug(
            "sendToGroupWithSessions(node=[omitted], jidsNeedSenderKey=%s, retryCount=%d)" % (jidsNeedSenderKey, retryCount)
        )
        jidsNeedSenderKey = jidsNeedSenderKey or []
        groupJid = node["to"]
        protoNode = node.getChild("proto")
        encEntities = []
        participant = jidsNeedSenderKey[0] if len(jidsNeedSenderKey) == 1 and retryCount > 0 else None
        if len(jidsNeedSenderKey):
            senderKeyDistributionMessage = self.manager.group_create_skmsg(groupJid)
            for jid in jidsNeedSenderKey:
                message =  self.serializeSenderKeyDistributionMessageToProtobuf(node["to"], senderKeyDistributionMessage)
                if retryCount > 0:
                    message.MergeFromString(protoNode.getData())
                ciphertext = self.manager.encrypt(jid.split('@')[0], message.SerializeToString())
                encEntities.append(
                    EncProtocolEntity(
                            EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG
                        , 2, ciphertext.serialize(), protoNode["mediatype"],  jid=None if participant else jid
                    )
                )

        if not retryCount:
            messageData = protoNode.getData()
            ciphertext = self.manager.group_encrypt(groupJid, messageData)
            mediaType = protoNode["mediatype"]

            encEntities.append(EncProtocolEntity(EncProtocolEntity.TYPE_SKMSG, 2, ciphertext, mediaType))

        self.sendEncEntities(node, encEntities, participant)

    def ensureSessionsAndSendToGroup(self, node, jids):
        logger.debug("ensureSessionsAndSendToGroup(node=[omitted], jids=%s)" % jids)
        jidsNoSession = []
        for jid in jids:
            if not self.manager.session_exists(jid.split('@')[0]):
                jidsNoSession.append(jid)

        if len(jidsNoSession):
            self.getKeysFor(jidsNoSession, lambda successJids, b: self.sendToGroupWithSessions(node, successJids))
        else:
            self.sendToGroupWithSessions(node, jids)

    def sendToGroup(self, node, retryReceiptEntity = None):
        logger.debug("sendToGroup(node=[omitted], retryReceiptEntity=[%s])" %
                     ("[retry_count=%s, retry_jid=%s]" % (
                         retryReceiptEntity.getRetryCount(), retryReceiptEntity.getRetryJid())
                      ) if retryReceiptEntity is not None else None)

        groupJid = node["to"]
        ownJid = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(True)

        senderKeyRecord = self.manager.load_senderkey(node["to"])

        def sendToGroup(resultNode, requestEntity):
            groupInfo = InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(resultNode)
            jids = list(groupInfo.getParticipants().keys()) #keys in py3 returns dict_keys
            if ownJid in jids:
                jids.remove(ownJid)
            return self.ensureSessionsAndSendToGroup(node, jids)

        if senderKeyRecord.isEmpty():
            logger.debug("senderKeyRecord is empty, requesting group info")
            groupInfoIq = InfoGroupsIqProtocolEntity(groupJid)
            self._sendIq(groupInfoIq, sendToGroup)
        else:
            logger.debug("We have a senderKeyRecord")
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
        m.sender_key_distribution_message.group_id = groupId
        m.sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        m.sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        # m.conversation = text
        return m
    ###
