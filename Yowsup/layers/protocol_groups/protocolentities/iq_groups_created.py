from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupsIqProtocolEntity
class CreatedGroupsIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq type="result" id="{{id}}" xmlns="w:g", to="g.us">
        <group id="{group_id}"></group>
    </iq>
    '''

    def __init__(self, subject, _id = None):
        super(CreateGroupIqProtocolEntity, self).__init__(to = "g.us", _id = _id, _type = "set")
        self.setProps(subject)

    def setProps(self, subject):
        self.subject = subject

    def toProtocolTreeNode(self):
        node = super(CreateGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("group",{"action": "create", "subject": self.subject}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = CreateGroupsIqProtocolEntity
        entity.setProps(node.getChild("group").getAttributeValue("subject"))
        return entity