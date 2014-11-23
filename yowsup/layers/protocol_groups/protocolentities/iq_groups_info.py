from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class InfoGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="get" to="g.us" xmlns="w:g">
        <query></query>
    </iq>


    '''

    def __init__(self):
        super(InfoGroupsIqProtocolEntity, self).__init__(to = "g.us", _id = _id, _type = "get")

    def toProtocolTreeNode(self):
        node = super(InfoGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("query"))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        assert node.getChild("query") is not None, "Not a goups info iq node %s" % node
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = InfoGroupsIqProtocolEntity
        return entity