from yowsup.structs import ProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from copy import deepcopy


class MessageProtocolEntity(ProtocolEntity):

    MESSAGE_TYPE_TEXT = "text"
    MESSAGE_TYPE_MEDIA = "media"

    def __init__(self, messageType, messageAttributes):
        """
        :type messageType: str
        :type messageAttributes: MessageAttributes
        """
        super(MessageProtocolEntity, self).__init__("message")
        assert type(messageAttributes) is MessageAttributes

        self._type = messageType
        self._id = messageAttributes.id or self._generateId()
        self._from = messageAttributes.sender
        self.to = messageAttributes.recipient
        self.timestamp = messageAttributes.timestamp or self._getCurrentTimestamp()
        self.notify = messageAttributes.notify
        self.offline = messageAttributes.offline
        self.retry = messageAttributes.retry
        self.participant= messageAttributes.participant

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

        if self.participant:
            attribs["participant"] = self.participant

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
        return OutgoingReceiptProtocolEntity(self.getId(), self.getFrom(), read, participant=self.getParticipant())

    def forward(self, to, _id = None):
        OutgoingMessage = deepcopy(self)
        OutgoingMessage.to = to
        OutgoingMessage._from = None
        OutgoingMessage._id = self._generateId() if _id is None else _id
        return OutgoingMessage

    @staticmethod
    def fromProtocolTreeNode(node):
        return MessageProtocolEntity(
            node["type"],
            MessageAttributes.from_message_protocoltreenode(node)
        )
