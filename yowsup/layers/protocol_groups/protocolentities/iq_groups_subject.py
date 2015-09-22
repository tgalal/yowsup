from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class SubjectGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g2", to={{group_jid}}">
        <subject>
              {{NEW_VAL}}
        </subject>
    </iq>
    '''
    def __init__(self, jid, subject, _id = None):
        super(SubjectGroupsIqProtocolEntity, self).__init__(to = jid, _id = _id, _type = "set")
        self.setProps(subject)

    def setProps(self, subject):
        self.subject = subject

    def toProtocolTreeNode(self):
        node = super(SubjectGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("subject",{}, None, self.subject))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(SubjectGroupsIqProtocolEntity, SubjectGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = SubjectGroupsIqProtocolEntity
        entity.setProps(node.getChild("subject").getData())
        return entity
