import time

from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
class OutgoingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    If we send the following without "to" specified, whatsapp will consider the message delivered,
    but will not notify the sender.
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    INCOMING
    <receipt offline="0" from="4915225256022@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, to, read = False, participant = None, callId = None):
        super(OutgoingReceiptProtocolEntity, self).__init__(_id)
        self.setOutgoingData(to, read, participant, callId)

    def setOutgoingData(self, to, read, participant, callId):
        self.to = to
        self.read = read
        self.participant = participant
        self.callId = callId
    
    def toProtocolTreeNode(self):
        node = super(OutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        if self.read:
            node.setAttribute("type", "read")
        if self.participant:
            node.setAttribute("participant", self.participant)
        if self.callId:
            offer = ProtocolTreeNode("offer", {"call-id": self.callId})
            node.addChild(offer)

        node.setAttribute("to", self.to)
        node.setAttribute("t", str(int(time.time())))

        return node

    def __str__(self):
        out = super(OutgoingReceiptProtocolEntity, self).__str__()
        out  += "To: \n%s" % self.to
        if self.read:
            out += "Type: \n%s" % "read"
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return OutgoingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("to"),
            node.getAttributeValue("type"),
            node.getAttributeValue("participant")
            )
