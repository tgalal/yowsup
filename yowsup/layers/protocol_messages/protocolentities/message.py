from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from copy import deepcopy

class MessageProtocolEntity(ProtocolEntity):

    MESSAGE_TYPE_TEXT = "text"
    MESSAGE_TYPE_MEDIA = "media"

    def __init__(self, _type, _id = None,  _from = None, to = None, notify = None, timestamp = None,
        participant = None, offline = None, retry = None):

        assert (to or _from), "Must specify either to or _from jids to create the message"
        assert not(to and _from), "Can't set both attributes to message at same time (to, _from)"


        super(MessageProtocolEntity, self).__init__("message")
        self._type          = _type
        self._id            = self._generateId() if _id is None else _id
        self._from          =_from
        self.to             = to
        self.timestamp      = int(timestamp) if timestamp else self._getCurrentTimestamp()
        self.notify         = notify
        self.offline        = offline == "1" if offline is not None else offline
        self.retry          = int(retry) if retry else None
        self.participant    = participant

    def getType(self):
        return self._type

    def getId(self):
        return self._id

    def getTimestamp(self):
        return self.timestamp

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]

    def isBroadcast(self):
        return False

    def getTo(self, full = True):
        return self.to if full else self.to.split('@')[0]

    def getParticipant(self, full = True):
        return self.participant if full else self.participant.split('@')[0]

    def getAuthor(self, full = True):
        return self.getParticipant(full) if self.isGroupMessage() else self.getFrom(full)

    def getNotify(self):
        return self.notify

    def toProtocolTreeNode(self):
        attribs = {
            "type"      : self._type,
            "id"        : self._id,
        }

        if self.isOutgoing():
            attribs["to"] = self.to
        else:
            attribs["from"] = self._from

            attribs["t"] = str(self.timestamp)

            if self.offline is not None:
               attribs["offline"] = "1" if self.offline else "0"
            if self.notify:
                attribs["notify"] = self.notify
            if self.retry:
                attribs["retry"] = str(self.retry)
            if self.participant:
                attribs["participant"] = self.participant


        xNode = None
        #if self.isOutgoing():
        #    serverNode = ProtocolTreeNode("server", {})
        #    xNode = ProtocolTreeNode("x", {"xmlns": "jabber:x:event"}, [serverNode])


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
        out += "Timestamp: %s\n" % self.timestamp
        if self.participant:
            out += "Participant: %s\n" % self.participant
        return out

    def ack(self, read=False):
        return OutgoingReceiptProtocolEntity(self.getId(), self.getFrom(), read, participant=self.getParticipant(), t=self.getTimestamp())

    def forward(self, to, _id = None):
        OutgoingMessage = deepcopy(self)
        OutgoingMessage.to = to
        OutgoingMessage._from = None
        OutgoingMessage._id = self._generateId() if _id is None else _id
        return OutgoingMessage

    @staticmethod
    def fromProtocolTreeNode(node):

        return MessageProtocolEntity(
            node.getAttributeValue("type"),
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("to"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("t"),
            node.getAttributeValue("participant"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry")
            )
