from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
class MessageProtocolEntity(ProtocolEntity):
    def __init__(self, _type, _id, _from, timestamp, notify, participant = None, offline = False, retry = None):
        super(MessageProtocolEntity, self).__init__("message")
        self._type          = _type
        self._id            = _id
        self._from          =_from
        self.timestmap      = int(timestamp)
        self.notify         = notify
        self.offline        = offline == "1"
        self.retry          = int(retry) if retry else None
        self.participant    = participant
    
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
        if self.participant:
            attribs["participant"] = participant
        return self._createProtocolTreeNode(attribs, children = None, data = None)

    def isGroupMessage(self):
        return self.participant != None

    def __str__(self):
        out  = "Message:\n"
        out += "From: %s\n" % self._from
        out += "Type:  %s\n" % self._type
        if self.participant:
            out += "Participant: %s\n" % self.participant
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return MessageProtocolEntity(
            node.getAttributeValue("type"), 
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("participant"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry")
            )
