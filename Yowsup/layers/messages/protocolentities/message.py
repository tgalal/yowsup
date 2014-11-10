from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
import time
class MessageProtocolEntity(ProtocolEntity):

    _ID_GEN = -1

    def __init__(self, _type, _id = None,  _from = None, to = None, notify = None, timestamp = None, 
        participant = None, offline = None, retry = None):

        if to is None and _from is None:
            raise ValueError("Must specify either to or _from jids to create the message")

        if to is not None and _from is not None:
            raise ValueError("Can't set both attributes to message at same time (to, _from)")

        super(MessageProtocolEntity, self).__init__("message")
        self._type          = _type
        self._id            = self.generateId() if _id is None else _id
        self._from          =_from
        self.to             = to
        self.timestamp      = int(timestamp) if timestamp else int(time.time())
        self.notify         = notify
        self.offline        = offline == "1" if offline is not None else offline
        self.retry          = int(retry) if retry else None
        self.participant    = participant

    def getType(self):
        return self._type

    def generateId(self):
        MessageProtocolEntity._ID_GEN += 1
        return str(int(time.time())) + "-" + str(MessageProtocolEntity._ID_GEN)
    
    def toProtocolTreeNode(self):
        attribs = {
            "type"      : self._type,
            "id"        : self._id,
        }

        if not self.isOutgoing():
            attribs["t"] = str(self.timestamp)

        if self.offline is not None:
            attribs["offline"] = "1" if self.offline else "0"

        if self.isOutgoing():
            attribs["to"] = self.to
        else:
            attribs["from"] = self._from

        if self.notify:
            attribs["notify"] = self.notify

        if self.retry:
            attribs["retry"] = str(self.retry)
        if self.participant:
            attribs["participant"] = participant


        xNode = None
        if self.isOutgoing():
            serverNode = ProtocolTreeNode("server", {})
            xNode = ProtocolTreeNode("x", {"xmlns": "jabber:x:event"}, [serverNode])


        return self._createProtocolTreeNode(attribs, children = [xNode] if xNode else None, data = None)

    def isOutgoing(self):
        return self._from is None

    def isGroupMessage(self):
        if self.isOutgoing():
            return "-" in self.to
        return self.participant != None

    def __str__(self):
        out  = "Message:\n"
        out += "ID: %s\n" % self._id
        out += "To: %s\n" % self.to  if self.isOutgoing() else "From: %s\n" % self._from 
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
            None,
            node.getAttributeValue("notify"),
            node.getAttributeValue("t"),
            node.getAttributeValue("participant"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry")
            )
