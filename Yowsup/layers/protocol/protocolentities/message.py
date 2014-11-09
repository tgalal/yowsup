from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
class MessageProtocolEntity(ProtocolEntity):
    def __init__(self, _type, _id, _from, timestamp, notify, offline, retry = None):
        super(MessageProtocolEntity, self).__init__("message")
        self._type      = _type
        self._id        = _id
        self._from      =_from
        self.timestmap  = int(timestamp)
        self.notify     = notify
        self.offline    = offline == "1"
        self.retry      = int(retry) if retry else None
    
    def toProtocolTreeNode(self):
        attribs = {
            "t"         : str(self.timestmap),
            "from"      : self._from,
            "offline"   : "1" if self.offline else "0",
            "type"      : self._type,
            "id"        : self._id,
            "notify"    : self.notify
        }
        if self.retry:
            attribs["retry"] = str(self.retry)
        return self._createProtocolTreeNode(attribs, children = None, data = None)

    @staticmethod
    def fromProtocolTreeNode(node):
        return MessageProtocolEntity(
            node.getAttributeValue("type"), 
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry")
            )
