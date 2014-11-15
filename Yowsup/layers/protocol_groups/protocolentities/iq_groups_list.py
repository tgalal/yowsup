from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupIqsProtocolEntity
class ListGroupsIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="get" to="g.us" xmlns="w:g">
        <list type="{{participating | owning}}"></list>
    </iq>
    '''

    GROUPS_TYPES = ("participating", "owning")

    def __init__(self, groupsType):
        super(ListGroupsIqProtocolEntity, self).__init__(to = "g.us", _id = _id, _type = "get")
        self.setProps(groupsType)

    def setProps(self, groupsType):
        assert groupsType in self.__class__.GROUPS_TYPES,
            "Groups type must be %s" % (" or ".join(self.__class__.GROUPS_TYPES))
        self.groupsType = groupsType

    def toProtocolTreeNode(self):
        node = super(ListGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("list",{"type": self.groupsType}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ListGroupsIqProtocolEntity
        entity.setProps(node.getChild("list").getAttributeValue("type"))
        return entity