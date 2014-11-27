from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ib import IbProtocolEntity
class DirtyIbProtocolEntity(IbProtocolEntity):
    '''
    <ib>
        <dirty type="{{groups | ?}}" timestamp="{{ts}}"></dirty>
    </ib>
    '''
    def __init__(self, timestamp, _type):
        super(DirtyIbProtocolEntity, self).__init__()
        self.setProps(timestamp, _type)


    def setProps(self, timestamp, _type):
        self.timestamp = int(timestamp)
        self._type = _type
    
    def toProtocolTreeNode(self):
        node = super(DirtyIbProtocolEntity, self).toProtocolTreeNode()
        dirtyNode = ProtocolTreeNode("dirty")
        dirtyNode["timestamp"] = str(self.timestamp)
        dirtyNode["type"] = self._type
        node.addChild(dirtyNode)
        return node

    def __str__(self):
        out = super(DirtyIbProtocolEntity, self).__str__()
        out += "Type: %s\n" % self._type
        out += "Timestamp: %s\n" % self.timestamp
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IbProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DirtyIbProtocolEntity
        dirtyChild = node.getChild("dirty")
        entity.setProps(dirtyChild["timestamp"], dirtyChild["type"])
        return entity
