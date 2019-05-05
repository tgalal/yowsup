from .layer_base import AxolotlBaseLayer

from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import *
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_messages.protocolentities.proto import ProtoProtocolEntity
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
from yowsup.axolotl import exceptions

from axolotl.untrustedidentityexception import UntrustedIdentityException

import logging
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
        except (exceptions.InvalidMessageException, exceptions.InvalidKeyIdException) as e:
            logger.warning("InvalidMessage or KeyId for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node, self.manager.registration_id)
            self.toLower(retry.toProtocolTreeNode())
        except exceptions.NoSessionException:
            logger.warning("No session for %s, getting their keys now", encMessageProtocolEntity.getAuthor(False))

            conversationIdentifier = (node["from"], node["participant"])

            if conversationIdentifier not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[conversationIdentifier] = []
            self.pendingIncomingMessages[conversationIdentifier].append(node)

            successFn = lambda successJids, b: self.processPendingIncomingMessages(*conversationIdentifier) if len(successJids) else None

            self.getKeysFor([senderJid], successFn)
        except exceptions.DuplicateMessageException:
            logger.warning("Received a message that we've previously decrypted, goint to send the delivery receipt myself")
            self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"], participant=node["participant"]).toProtocolTreeNode())

        except UntrustedIdentityException as e:
            if self.getProp(PROP_IDENTITY_AUTOTRUST, False):
                logger.warning("Autotrusting identity for %s", e.getName())
                self.manager.trust_identity(e.getName(), e.getIdentityKey())
                return self.handleEncMessage(node)
            else:
                logger.error("Ignoring message with untrusted identity")

    def handlePreKeyWhisperMessage(self, node):
        pkMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = pkMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG)
        plaintext = self.manager.decrypt_pkmsg(pkMessageProtocolEntity.getAuthor(False), enc.getData(),
                                               enc.getVersion() == 2)

        if enc.getVersion() == 2:
            self.parseAndHandleMessageProto(pkMessageProtocolEntity, plaintext)

        node = pkMessageProtocolEntity.toProtocolTreeNode()
        node.addChild((ProtoProtocolEntity(plaintext, enc.getMediaType())).toProtocolTreeNode())

        self.toUpper(node)

    def handleWhisperMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)

        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG)
        plaintext = self.manager.decrypt_msg(encMessageProtocolEntity.getAuthor(False), enc.getData(),
                                             enc.getVersion() == 2)

        if enc.getVersion() == 2:
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)

        node = encMessageProtocolEntity.toProtocolTreeNode()
        node.addChild((ProtoProtocolEntity(plaintext, enc.getMediaType())).toProtocolTreeNode())

        self.toUpper(node)

    def handleSenderKeyMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG)

        try:
            plaintext = self.manager.group_decrypt (
                groupid=encMessageProtocolEntity.getFrom(True),
                participantid=encMessageProtocolEntity.getParticipant(False),
                data=enc.getData()
            )
            plaintext = plaintext.encode() if sys.version_info >= (3, 0) else plaintext
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)

            node = encMessageProtocolEntity.toProtocolTreeNode()
            node.addChild((ProtoProtocolEntity(plaintext, enc.getMediaType())).toProtocolTreeNode())

            self.toUpper(node)

        except exceptions.NoSessionException:
            logger.warning("No session for %s, going to send a retry", encMessageProtocolEntity.getAuthor(False))
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node, self.manager.registration_id)
            self.toLower(retry.toProtocolTreeNode())
        except exceptions.DuplicateMessageException:
            logger.warning(
                "Received a message that we've previously decrypted, goint to send the delivery receipt myself"
            )
            self.toLower(
                OutgoingReceiptProtocolEntity(
                    node["id"], node["from"], participant=node["participant"]
                ).toProtocolTreeNode()
            )

    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        m = Message()
        try:
            m.ParseFromString(serializedData)
        except:
            print("DUMP:")
            print(serializedData)
            print([s for s in serializedData])
            # print([ord(s) for s in serializedData])
            raise
        if not m or not serializedData:
            raise ValueError("Empty message")

        if m.HasField("sender_key_distribution_message"):
            self.handleSenderKeyDistributionMessage(
                m.sender_key_distribution_message,
                encMessageProtocolEntity.getParticipant(False)
            )

    def handleSenderKeyDistributionMessage(self, senderKeyDistributionMessage, participantId):
        groupId = senderKeyDistributionMessage.group_id
        self.manager.group_create_session(
            groupid=groupId,
            participantid=participantId,
            skmsgdata=senderKeyDistributionMessage.axolotl_sender_key_distribution_message
        )


