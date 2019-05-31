from yowsup.layers import YowProtocolLayer
from .protocolentities import TextMessageProtocolEntity
from .protocolentities import ExtendedTextMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.converter import AttributesConverter
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity

import logging
logger = logging.getLogger(__name__)


class YowMessagesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity)
        }
        super(YowMessagesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Messages Layer"

    def sendMessageEntity(self, entity):
        if entity.getType() == "text":
            self.entityToLower(entity)

    ###recieved node handlers handlers
    def recvMessageStanza(self, node):
        protoNode = node.getChild("proto")

        if protoNode:
            if protoNode and protoNode["mediatype"] is None:
                message = AttributesConverter.get().protobytes_to_message(protoNode.getData())
                if message.conversation:
                    self.toUpper(
                        TextMessageProtocolEntity(
                            message.conversation, MessageMetaAttributes.from_message_protocoltreenode(node)
                        )
                    )
                elif message.extended_text:
                    self.toUpper(
                        ExtendedTextMessageProtocolEntity(
                            message.extended_text,
                            MessageMetaAttributes.from_message_protocoltreenode(node)
                        )
                    )
                elif not message.sender_key_distribution_message:
                    # Will send receipts for unsupported message types to prevent stream errors
                    logger.warning("Unsupported message type: %s, will send receipts to "
                                   "prevent stream errors" % message)
                    self.toLower(
                        OutgoingReceiptProtocolEntity(
                            messageIds=[node["id"]],
                            to=node["from"],
                            participant=node["participant"]
                        ).toProtocolTreeNode()
                    )
