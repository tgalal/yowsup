from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupIqProtocolEntity
class SubjectGroupIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to={{group_jid}}">
        <subject value="{{NEW_VAL}}"></subject>
    </iq>
    '''
    def __init__(self, jid, subject, _id = None):
        super(SubjectGroupIqProtocolEntity, self).__init__(_to = jid, _id = _id, _type = "set")
        self.setProps(subject)

    def setProps(self, subject):
        self.subject = subject

    def toProtocolTreeNode(self):
        node = super(SubjectGroupIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("subject",{"value": self.subject}))

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SubjectGroupIqProtocolEntity
        entity.setProps(node.getChild("subject").getAttributeValue("value"))