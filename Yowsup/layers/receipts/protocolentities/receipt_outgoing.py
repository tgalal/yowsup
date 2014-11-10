from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
class OutgoingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    INCOMING
    <receipt offline="0" from="4915225256022@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, to, _type = None):
        super(OutgoingReceiptProtocolEntity, self).__init__(_id)
        self.setOutgoingData(to, _type)

    def setOutgoingData(self, to, _type):
        self.to = to
        self._type = _type
    
    def toProtocolTreeNode(self):
        node = super(OutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        if self._type:
            node.setAttribute("type", self._type)
        return node

    def __str__(self):
        out = super(OutgoingReceiptProtocolEntity, self).__str__()
        out  += "To: \n%s" % self.to
        if self._type:
            out += "Type: \n%s" % self._type
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return OutgoingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("to"),
            node.getAttributeValue("type")
            )
