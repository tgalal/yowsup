from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_groups.protocolentities import InfoGroupsIqProtocolEntity, InfoGroupsResultIqProtocolEntity
from axolotl.protocol.whispermessage import WhisperMessage
from yowsup.layers.protocol_messages.protocolentities.message import MessageMetaAttributes
from yowsup.layers.axolotl.protocolentities.iq_keys_get_result import MissingParametersException
from yowsup.axolotl import exceptions
from .layer_base import AxolotlBaseLayer

import logging

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

    def send(self, node):
        if node.tag == "message" and node["to"] not in self.skipEncJids:
            self.processPlaintextNodeAndSend(node)
        else:
            self.toLower(node)

    def receive(self, protocolTreeNode):

        def on_get_keys_success(node, retry_entity, success_jids, errors):
            if len(errors):
                self.on_get_keys_process_errors(errors)
            elif len(success_jids) == 1:
                self.processPlaintextNodeAndSend(node, retry_entity)
            else:
                raise NotImplementedError()

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
                        lambda successJids, errors: on_get_keys_success(messageNode, retryReceiptEntity, successJids, errors)
                    )
                else:
                    #not interested in any non retry receipts, bubble upwards
                    self.toUpper(protocolTreeNode)

    def on_get_keys_process_errors(self, errors):
        # type: (dict) -> None
        for jid, error in errors.items():
            if isinstance(error, MissingParametersException):
                logger.error("Failed to create prekeybundle for %s, user had missing parameters: %s, "
                             "is that a valid user?" % (jid, error.parameters))
            elif isinstance(error, exceptions.UntrustedIdentityException):
                logger.error("Failed to create session for %s as user's identity is not trusted. " % jid)
            else:
                logger.error("Failed to process keys for %s, is that a valid user? Exception: %s" % error)

    def processPlaintextNodeAndSend(self, node, retryReceiptEntity = None):
        recipient_id = node["to"].split('@')[0]
        isGroup = "-" in recipient_id

        def on_get_keys_error(error_node, getkeys_entity, plaintext_node):
            logger.error("Failed to fetch keys for %s, is that a valid user? "
                         "Server response: [code=%s, text=%s], aborting send." % (
                plaintext_node["to"], error_node.children[0]["code"], error_node.children[0]["text"]
            ))

        def on_get_keys_success(node, success_jids, errors):
            if len(errors):
                self.on_get_keys_process_errors(errors)
            elif len(success_jids) == 1:
                self.sendToContact(node)
            else:
                raise NotImplementedError()

        if isGroup:
            self.sendToGroup(node, retryReceiptEntity)
        elif self.manager.session_exists(recipient_id):
            self.sendToContact(node)
        else:
            self.getKeysFor(
                [node["to"]],
                lambda successJids, errors: on_get_keys_success(node, successJids, errors),
                lambda error_node, entity: on_get_keys_error(error_node, entity, node)
            )

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
        message_attrs = MessageMetaAttributes.from_message_protocoltreenode(node)
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

        def on_get_keys_success(node, success_jids, errors):
            if len(errors):
                self.on_get_keys_process_errors(errors)

            self.sendToGroupWithSessions(node, success_jids)

        if len(jidsNoSession):
            self.getKeysFor(jidsNoSession, lambda successJids, errors: on_get_keys_success(node, successJids, errors))
        else:
            self.sendToGroupWithSessions(node, jids)

    def sendToGroup(self, node, retryReceiptEntity = None):
        """
        Group send sequence:
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
        """
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

    def serializeSenderKeyDistributionMessageToProtobuf(self, groupId, senderKeyDistributionMessage, message = None):
        m = message or Message()
        m.sender_key_distribution_message.group_id = groupId
        m.sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        m.sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        # m.conversation = text
        return m
