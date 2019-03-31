from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity

class NotificationProtocolEntity(ProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="{{NOTIFICATION_TYPE}}" 
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
    </notification>

    
    '''
    def __init__(self, _type, _id, _from, timestamp, notify, offline):
        super(NotificationProtocolEntity, self).__init__("notification")
        self._type      = _type
        self._id        = _id
        self._from      =_from
        self.timestamp  = int(timestamp)
        self.notify     = notify
        self.offline    = offline == "1"
   

    def __str__(self):
        out = "Notification\n"
        out += "From: %s\n" % self.getFrom()
        out += "Type: %s\n" % self.getType()
        return out

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]

    def getType(self):
        return self._type

    def getId(self):
        return self._id

    def getTimestamp(self):
        return self.timestamp

    def toProtocolTreeNode(self):
        attribs = {
            "t"         : str(self.timestamp),
            "from"      : self._from,
            "offline"   : "1" if self.offline else "0",
            "type"      : self._type,
            "id"        : self._id,
            "notify"    : self.notify
        }
       
        return self._createProtocolTreeNode(attribs, children = None, data = None)

    @staticmethod
    def fromProtocolTreeNode(node):
        return NotificationProtocolEntity(
            node.getAttributeValue("type"), 
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("offline")
            )
