from yowsup.common import YowConstants
from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class LeaveGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="set" to="{{group_jid}}" xmlns="w:g2">
        <leave action="delete">
		    <group id="{{JID}}">
            <group id="{{JID}}">
        </leave>
    </iq>
    '''

    def __init__(self, groupList):
        super(LeaveGroupsIqProtocolEntity, self).__init__(to = YowConstants.WHATSAPP_GROUP_SERVER, _type = "set")
        self.setProps(groupList if type(groupList) is list else [groupList])

    def setProps(self, groupList):
        assert type(groupList) is list and len(groupList), "Must specify a list of group jids to leave"
        self.groupList = groupList

    def toProtocolTreeNode(self):
        node = super(LeaveGroupsIqProtocolEntity, self).toProtocolTreeNode()
        groupNodes = [
            ProtocolTreeNode("group", {
                "id":       groupid
            })
            for groupid in self.groupList
        ]
        node.addChild(ProtocolTreeNode("leave", {"action": "delete"}, groupNodes))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        assert node.getChild("leave") is not None, "Not a group leave iq node %s" % node
        assert node.getChild("leave").getAttributeValue("action") == "delete", "Not a group leave action %s" % node
        entity = super(LeaveGroupsIqProtocolEntity, LeaveGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = LeaveGroupsIqProtocolEntity
        entity.setProps([group.getAttributeValue("id") for group in node.getChild("leave").getAllChildren()] )
        return entity
