from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class AckProtocolEntity(ProtocolEntity):

    '''
    <ack class="{{receipt | message | ?}}" id="{{message_id}}">
    </ack>
    '''

    def __init__(self, _id, _class):
        super(AckProtocolEntity, self).__init__("ack")
        self._id = _id
        self._class = _class

    def getId(self):
        return self._id

    def getClass(self):
        return self._class
    
    def toProtocolTreeNode(self):
        attribs = {
            "id"           : self._id,
            "class"        : self._class,
        }

        return self._createProtocolTreeNode(attribs, None, data = None)

    def __str__(self):
        out  = "ACK:\n"
        out += "ID: %s\n" % self._id
        out += "Class: %s\n" % self._class
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return AckProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("class")
            )
