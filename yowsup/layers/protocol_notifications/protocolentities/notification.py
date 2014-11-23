from yowsup.structs import ProtocolEntity, ProtocolTreeNode
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
        self.timestmap  = int(timestamp)
        self.notify     = notify
        self.offline    = offline == "1"
   
    
    def getFrom(self):
        return self._from

    def getType(self):
        return self._type

    def getId(self):
        return self._id

    def toProtocolTreeNode(self):
        attribs = {
            "t"         : str(self.timestmap),
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
