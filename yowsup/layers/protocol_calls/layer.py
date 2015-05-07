from yowsup.layers import YowProtocolLayer
from .protocolentities import *
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
class YowCallsProtocolLayer(YowProtocolLayer):

    def __init__(self):
        handleMap = {
            "call": (self.recvCall, self.sendCall)
        }
        super(YowCallsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "call Layer"

    def sendCall(self, entity):
        if entity.getTag() == "call":
            self.toLower(entity.toProtocolTreeNode())

    def recvCall(self, node):
        entity = CallProtocolEntity.fromProtocolTreeNode(node)
        if entity.getType() == "offer":
            receipt = OutgoingReceiptProtocolEntity(node["id"], node["from"], callId = entity.getCallId())
            self.toLower(receipt.toProtocolTreeNode())
        else:
            ack = OutgoingAckProtocolEntity(node["id"], "call", None, node["from"])
            self.toLower(ack.toProtocolTreeNode())
        self.toUpper(entity)

