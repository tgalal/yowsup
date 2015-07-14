from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
from ..structs import Group
class ListGroupsResultIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" from="g.us" id="{{IQ_ID}}">
      <groups>
          <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" creator="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
            <participant jid="{{JID}}" type="admin">
            </participant>
            <participant jid="{{JID}}">
            </participant>
          </group>
          <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" creator="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
            <participant jid="{{JID}}" type="admin">
            </participant>
          </group>
      <groups>
    </iq>
    '''

    def __init__(self, groupsList):
        super(ListGroupsResultIqProtocolEntity, self).__init__(_from = "g.us")
        self.setProps(groupsList)

    def __str__(self):
        out = super(ListGroupsResultIqProtocolEntity, self).__str__()
        out += "Groups:\n"
        for g in self.groupsList:
            out += "%s\n" % g
        return out

    def getGroups(self):
        return self.groupsList

    def setProps(self, groupsList):
        assert type(groupsList) is list and (len(groupsList) == 0 or groupsList[0].__class__ is Group),\
            "groupList must be a list of Group instances"
        self.groupsList = groupsList


    def toProtocolTreeNode(self):
        node = super(ListGroupsResultIqProtocolEntity, self).toProtocolTreeNode()
        groupsNodes = [
            ProtocolTreeNode("group", {
                "id":       group.getId(),
                "creator":    group.getCreator(),
                "subject":  group.getSubject(),
                "s_o":      group.getSubjectOwner(),
                "s_t":      str(group.getSubjectTime()),
                "creation": str(group.getCreationTime())
                })
            for group in self.groupsList
        ]
        node.addChild(ProtocolTreeNode("groups",{}, groupsNodes))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(ListGroupsResultIqProtocolEntity, ListGroupsResultIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = ListGroupsResultIqProtocolEntity
        groups = [
            Group(groupNode["id"], groupNode["creator"], groupNode["subject"], groupNode["s_o"], groupNode["s_t"], groupNode["creation"])
            for groupNode in node.getChild("groups").getAllChildren()
        ]
        entity.setProps(groups)
        return entity
