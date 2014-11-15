from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupIqProtocolEntity
class CreateGroupIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to="g.us">
        <group action="create" subject="{{subject}}"></group>
    </iq>
    '''

    def __init__(self, subject, _id = None):
        super(CreateGroupIqProtocolEntity, self).__init__(to = "g.us", _id = _id, _type = "set")
        self.setProps(subject)

    def setProps(self, subject):
        self.subject = subject

    def toProtocolTreeNode(self):
        node = super(CreateGroupIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("group",{"action": "create", "subject": self.subject}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = CreateGroupIqProtocolEntity
        entity.setProps(node.getChild("group").getAttributeValue("subject"))
        return entity