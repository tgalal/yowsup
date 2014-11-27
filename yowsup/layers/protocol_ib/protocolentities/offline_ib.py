from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ib import IbProtocolEntity
class OfflineIbProtocolEntity(IbProtocolEntity):
    '''
    <ib from="s.whatsapp.net">
        <offline count="{{X}}"></offline>
    </ib>
    '''
    def __init__(self, count):
        super(IbProtocolEntity, self).__init__()
        self.setProps(count)


    def setProps(self, count):
        self.count = int(count)
    
    def toProtocolTreeNode(self):
        node = super(OfflineIbProtocolEntity, self).toProtocolTreeNode()
        offlineChild = ProtocolTreeNode("offline", {"count": str(self.count)})
        node.addChild(offlineChild)
        return node

    def __str__(self):
        out = super(OfflineIbProtocolEntity, self).__str__()
        out += "Offline count: %s\n" % self.count
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IbProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = OfflineIbProtocolEntity
        entity.setProps(node.getChild("offline")["count"])
        return entity
