from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupIqProtocolEntity
class LeaveGroupIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to="g.us">
        <leave>
            <group id="{{gjid}}"></group>
        <leave>
    </iq>
    '''

    def __init__(self, jids, _id = None):
        super(LeaveGroupIqProtocolEntity, self).__init__(_to = "g.us", _id = _id, _type = "set")
        self.setProps(jids)

    def setProps(self, jids):
        self.jids = jids

    def toProtocolTreeNode(self):
        node = super(LeaveGroupIqProtocolEntity, self).toProtocolTreeNode()
        leaveNode = ProtocolTreeNode("leave",{}, [ProtocolTreeNode("group", {"id": jid}) for jid in self.jids])
        node.addChild(leaveNode)

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = LeaveGroupIqProtocolEntity
        entity.setProps([group.getAttributeValue("id") for group in node.getChild("leave").getAllChildren()])