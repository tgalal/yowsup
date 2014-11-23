from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class DeleteGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="set" to="{{group_jid}}" xmlns="w:g">
        <group action="delete"></query>
    </iq>
    '''

    def __init__(self, groupJid):
        super(InfoGroupsIqProtocolEntity, self).__init__(to = groupJid, _id = _id, _type = "set")
        self.setProps(groupJid)

    def setProps(self, groupJid):
        self.groupJid = groupJid

    def toProtocolTreeNode(self):
        node = super(DeleteGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("group", {"action": "delete"}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        assert node.getChild("group") is not None, "Not a group delete iq node %s" % node
        assert node.getChild("group").getAttributeValue("action") == "delete", "Not a group delete action %s" % node
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DeleteGroupsIqProtocolEntity
        return entity