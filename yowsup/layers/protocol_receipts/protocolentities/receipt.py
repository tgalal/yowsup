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

    def __init__(self, _id):
        super(ReceiptProtocolEntity, self).__init__("receipt")
        self._id = _id

    def getId(self):
        return self._id
    
    def toProtocolTreeNode(self):
        attribs = {
            "id"           : self._id
        }
        return self._createProtocolTreeNode(attribs, None, data = None)


    def __str__(self):
        out  = "Receipt:\n"
        out += "ID: %s\n" % self._id
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return ReceiptProtocolEntity(
            node.getAttributeValue("id")
            )
