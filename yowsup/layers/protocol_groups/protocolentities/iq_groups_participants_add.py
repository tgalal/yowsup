from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity


class AddParticipantsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to="{{group_jid}}">
        <add>
            <participant jid="{{jid}}""></participant>
        </add>
    </iq>
    '''

    def __init__(self, group_jid, jid = None, _id = None):
        super(AddParticipantsIqProtocolEntity, self).__init__(to = group_jid, _id = _id, _type = "set")
        self.setProps(group_jid, jid)

    def setProps(self, group_jid, jid):
        self.group_jid = group_jid
        self.jid = jid

    def toProtocolTreeNode(self):
        node = super(AddParticipantsIqProtocolEntity, self).toProtocolTreeNode()
        node_add_label = ProtocolTreeNode("add")
        node_participant_label = ProtocolTreeNode("participant", {"jid": self.jid})

        node_add_label.addChild(node_participant_label)
        node.addChild(node_add_label)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AddParticipantsIqProtocolEntity
        entity.setProps(node.getChild("add").node.getChild("participant").getAttributeValue("jid"))
        return entity