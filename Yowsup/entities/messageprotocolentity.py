from protocolentity import ProtocolEntity
from protocoltreenode import ProtocolTreeNode
class MessageProtocolEntity(ProtocolEntity):

    def __init__(self, _id, _from, _timestamp, _notify):
        self._id = _id
        self._from = _from
        self._timestamp = _timestamp
        self._notify = _notify

    def fromProtocolTreeNode(self, node):
         messageArgs = (
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify")
        )
        return MessageProtocolEntity(*messageArgs)
    def toProtocolTreeNode(self):
        return ""
