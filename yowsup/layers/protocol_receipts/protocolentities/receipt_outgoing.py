import time

from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
class OutgoingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    If we send the following without "to" specified, whatsapp will consider the message delivered,
    but will not notify the sender.
    t is the time the original message was sent.
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" t="xxxxxxxx"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read" t="xxxxxxxxx"></receipt>

    multiple items:
    <receipt type="read" to="xxxxxxxxxxxx@s.whatsapp.net" id="1431364583-191">
        <list>
            <item id="1431364572-189"></item>
            <item id="1431364575-190"></item>
        </list>
    </receipt>
    '''


    def __init__(self, messageIds, to, read = False, participant = None, callId = None, t = None):
        if type(messageIds) in (list, tuple):
            if len(messageIds) > 1:
                receiptId = self._generateId()
            else:
                receiptId = messageIds[0]
        else:
            receiptId = messageIds
            messageIds = [messageIds]

        super(OutgoingReceiptProtocolEntity, self).__init__(receiptId)
        self.setOutgoingData(messageIds, to, read, participant, callId, t)

    def setOutgoingData(self, messageIds, to, read, participant, callId, t):
        self.messageIds = messageIds
        self.to = to
        self.read = read
        self.participant = participant
        self.callId = callId
        self.t = t

    def getMessageIds(self):
        return self.messageIds

    def toProtocolTreeNode(self):
        node = super(OutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        if self.read:
            node.setAttribute("type", "read")
        if self.participant:
            node.setAttribute("participant", self.participant)
        if self.callId:
            offer = ProtocolTreeNode("offer", {"call-id": self.callId})
            node.addChild(offer)
        if self.t:
            node.setAttribute("t", str(self.t))

        node.setAttribute("to", self.to)

        if len(self.messageIds) > 1:
            listNode = ProtocolTreeNode("list")
            listNode.addChildren([ProtocolTreeNode("item", {"id": mId}) for mId in self.messageIds])
            node.addChild(listNode)

        return node

    def __str__(self):
        out = super(OutgoingReceiptProtocolEntity, self).__str__()
        out  += "To: \n%s" % self.to
        if self.read:
            out += "Type: \n%s" % "read"
        out += "For: \n%s" % self.messageIds
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        listNode = node.getChild("list")
        messageIds = []
        if listNode:
            messageIds = [child["id"] for child in listNode.getChildren()]
        else:
            messageIds = [node["id"]]

        return OutgoingReceiptProtocolEntity(
            messageIds,
            node["to"],
            node["type"] == "read",
            node["participant"],
            t=node["t"]
            )
