from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_result_groups import GroupsResultIqProtocolEntity
from ..structs import Group
class ListGroupsResultIqProtocolEntity(GroupsResultIqProtocolEntity):
    '''
    <iq type="result" from="g.us" id="{{IQ_ID}}">
        <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" owner="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
        </group>
        <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" owner="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
        </group>
    </iq>
    '''

    def __init__(self, groupsList):
        super(ListGroupsResultIqProtocolEntity, self).__init__(_from = "g.us")
        self.setProps(groupsList)

    def __str__(self):
        out = super(ListGroupsResultIqProtocolEntity, self).__str__()
        for g in self.groupsList:
            out += "%s" % g
            out += "\n"
        return out

    def setProps(self, groupsList):
        assert type(groupsList) is list and len(groupsList) > 0 and groupsList[0].__class__ is Group,\
            "groupList must be a list of Group instances"
        self.groupsList = groupsList


    def toProtocolTreeNode(self):
        node = super(ListGroupsResultIqProtocolEntity, self).toProtocolTreeNode()

        groupsNodes = [
            ProtocolTreeNode("group", {
                "id":       group.getId(),
                "owner":    group.getOwner(),
                "subject":  group.getSubject(),
                "s_o":      group.getSubjectOwner(),
                "s_t":      str(group.getSubjectTime()),
                "creation": str(group.getCreationTime())
                })
            for group in self.groupsList
        ]

        node.addChildren(groupsNodes)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsResultIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ListGroupsResultIqProtocolEntity
        groups = [
            Group(groupNode["id"], groupNode["owner"], groupNode["subject"], groupNode["s_o"], groupNode["s_t"], groupNode["creation"])
            for groupNode in node.getAllChildren()
        ]
        entity.setProps(groups)
        return entity