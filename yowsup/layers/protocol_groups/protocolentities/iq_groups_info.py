from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class InfoGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="get" to="{{group_jid}}" xmlns="w:g2">
        <query request="interactive"></query>
    </iq>


    '''

    def __init__(self, group_jid, _id=None):
        super(InfoGroupsIqProtocolEntity, self).__init__(to = group_jid, _id = _id, _type = "get")
        self.setProps(group_jid)

    def setProps(self, group_jid):
        self.group_jid = group_jid

    def __str__(self):
        out = super(InfoGroupsIqProtocolEntity, self).__str__()
        out += "Group JID: %s\n" % self.group_jid
        return out

    def toProtocolTreeNode(self):
        node = super(InfoGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("query", {"request": "interactive"}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        assert node.getChild("query") is not None, "Not a groups info iq node %s" % node
        entity = super(InfoGroupsIqProtocolEntity, InfoGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = InfoGroupsIqProtocolEntity
        entity.setProps(node.getAttributeValue("to"))
        return entity
