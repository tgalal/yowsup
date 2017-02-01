from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ReceiptProtocolEntity(ProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read || played"></receipt>

    INCOMING
    <receipt offline="0" from="4915225256022@s.whatsapp.net" id="1415577964-1" t="1415578027" type="played?"></receipt>
    '''

    def __init__(self, _id, _type = None, _from = None, to = None, timestamp = None):
        super(ReceiptProtocolEntity, self).__init__("receipt")
        self._id = _id
        self._type = _type
        self._from = _from
        self.to = to

    def getType(self):
        return self._type

    def getId(self):
        return self._id

    def getTimestamp(self):
        return self.timestamp

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]
        
    def getTo(self, full = True):
        return self.to if full else self.to.split('@')[0]
        
    def toProtocolTreeNode(self):
        attribs = {
            "id"           : self._id
        }
        
        if self._type:
            attribs["type"] = self._type
        
        if self.isOutgoing():
            attribs["to"] = self.to
        else:
            attribs["from"] = self._from
            
        return self._createProtocolTreeNode(attribs, None, data = None)

    def isOutgoing(self):
        return self._from is None

    def __str__(self):
        out  = "Receipt:\n"
        out += "ID: %s\n" % self._id
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return ReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("type"),
            node.getAttributeValue("from"),
            node.getAttributeValue("to"),
            node.getAttributeValue("t")
            )
