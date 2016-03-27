from yowsup.common import YowConstants
from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class ListGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq id="{{id}}"" type="get" to="g.us" xmlns="w:g2">
        <"{{participating | owning}}"></"{{participating | owning}}">
    </iq>
    
    result (processed in iq_result_groups_list.py):
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

    GROUP_TYPE_PARTICIPATING = "participating"
    GROUP_TYPE_OWNING        = "owning"

    GROUPS_TYPES = (GROUP_TYPE_PARTICIPATING, GROUP_TYPE_OWNING)

    def __init__(self, groupsType = GROUP_TYPE_PARTICIPATING, _id = None):
        super(ListGroupsIqProtocolEntity, self).__init__(_id=_id, to = YowConstants.WHATSAPP_GROUP_SERVER, _type = "get")
        self.setProps(groupsType)

    def setProps(self, groupsType):
        assert groupsType in self.__class__.GROUPS_TYPES,\
            "Groups type must be %s, not %s" % (" or ".join(self.__class__.GROUPS_TYPES), groupsType)
        self.groupsType = groupsType

    def toProtocolTreeNode(self):
        node = super(ListGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode(self.groupsType))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(ListGroupsIqProtocolEntity, ListGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = ListGroupsIqProtocolEntity
        entity.setProps(node.getChild(0).tag)
        return entity
