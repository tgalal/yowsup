from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class CallProtocolEntity(ProtocolEntity):
    '''
    <call offline="0" from="{{CALLER_JID}}" id="{{ID}}" t="{{TIMESTAMP}}" notify="{{CALLER_PUSHNAME}}" retry="{{RETRY}}" e="{{?}}">
    </call>
    
    '''
    def __init__(self, _id, _type, timestamp, notify = None, offline = None, retry = None, e = None, callId = None, _from = None, _to = None):
        super(CallProtocolEntity, self).__init__("call")
        self._id            = _id or self._generateId()
        self._type       = _type
        self._from      = _from
        self._to           = _to
        self.timestamp  = int(timestamp)
        self.notify     = notify
        self.offline    = offline == "1"
        self.retry      = retry
        self.e             = e
        self.callId     = callId

    def __str__(self):
        out = "Call\n"
        if self.getFrom() is not None:
            out += "From: %s\n" % self.getFrom()
        if self.getTo() is not None:
            out += "To: %s\n" % self.getTo()
        if self.getType() is not None:
            out += "Type: %s\n" % self.getType()
        if self.getCallId() is not None:
            out += "Call ID: %s\n" % self.getCallId()
        return out

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]
        
    def getTo(self):
        return self._to

    def getId(self):
        return self._id
        
    def getType(self):
        return self._type
        
    def getCallId(self):
        return self.callId

    def getTimestamp(self):
        return self.timestamp

    def toProtocolTreeNode(self):
        children = []
        attribs = {
            "t"         : str(self.timestamp),
            "offline"   : "1" if self.offline else "0",
            "id"        : self._id,
        }
        if self._from is not None:
            attribs["from"] = self._from
        if self._to is not None:
            attribs["to"] = self._to
        if self.retry is not None:
            attribs["retry"] = self.retry
        if self.e is not None:
            attribs["e"] = self.e
        if self.notify is not None:
            attribs["notify"] = self.notify
        if self._type in ["offer", "transport", "relaylatency", "reject", "terminate"]:
            child = ProtocolTreeNode(self._type, {"call-id": self.callId})
            children.append(child)
        return self._createProtocolTreeNode(attribs, children = children, data = None)

    @staticmethod
    def fromProtocolTreeNode(node):
        (_type, callId) = [None] * 2
        offer = node.getChild("offer")
        transport = node.getChild("transport")
        relaylatency = node.getChild("relaylatency")
        reject = node.getChild("reject")
        terminate = node.getChild("terminate")
        if offer:
            _type = "offer"
            callId = offer.getAttributeValue("call-id")
        elif transport:
            _type = "transport"
            callId = transport.getAttributeValue("call-id")
        elif relaylatency:
            _type = "relaylatency"
            callId = relaylatency.getAttributeValue("call-id")
        elif reject:
            _type = "reject"
            callId = reject.getAttributeValue("call-id")
        elif terminate:
            _type = "terminate"
            callId = terminate.getAttributeValue("call-id")
        return CallProtocolEntity(
            node.getAttributeValue("id"),
            _type,
            node.getAttributeValue("t"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("retry"),
            node.getAttributeValue("e"),
            callId,
            node.getAttributeValue("from"),
            node.getAttributeValue("to")
            )
