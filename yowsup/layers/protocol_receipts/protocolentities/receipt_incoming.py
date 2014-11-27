from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
class IncomingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    INCOMING
    <receipt offline="0" from="xxxxxxxxxx@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, _from, timestamp, offline = None):
        super(IncomingReceiptProtocolEntity, self).__init__(_id)
        self.setIncomingData(_from, timestamp, offline)

    def setIncomingData(self, _from, timestamp, offline):
        self._from = _from
        self.timestamp = timestamp
        if offline is not None:
            self.offline = True if offline == "1" else False
        else:
            self.offline = None
    
    def toProtocolTreeNode(self):
        node = super(IncomingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("from", self._from)
        node.setAttribute("timestamp", self.timestamp)
        if self.offline is not None:
            node.setAttribute("1" if self.offline else "0")
        return node

    def __str__(self):
        out = super(IncomingReceiptProtocolEntity, self).__str__()
        out += "From: \n%s" % self._from
        out += "Timestamp: \n%s" % self.timestamp
        if self.offline is not None:
            out += "Offline: %s\n" % ("1" if self.offline else "0")
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return IncomingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("timestamp"),
            node.getAttributeValue("offline"    )
            )