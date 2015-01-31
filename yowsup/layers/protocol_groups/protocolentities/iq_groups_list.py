from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class ListGroupsIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_groups_list.xsd")
    '''
    <iq id="{{id}}"" type="get" to="g.us" xmlns="w:g">
        <list type="{{participating | owning}}"></list>
    </iq>
    
    result (processed in iq_result_groups_list.py):
    <iq type="result" from="g.us" id="{{IQ_ID}}">
        <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" owner="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
        </group>
        <group s_t="{{SUBJECT_TIME}}" creation="{{CREATING_TIME}}" owner="{{OWNER_JID}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}" subject="{{SUBJECT}}">
        </group>
    </iq>
    '''

    GROUP_TYPE_PARTICIPATING = "participating"
    GROUP_TYPE_OWNING        = "owning"

    GROUPS_TYPES = (GROUP_TYPE_PARTICIPATING, GROUP_TYPE_OWNING)

    def __init__(self, groupsType = GROUP_TYPE_PARTICIPATING, _id = None):
        super(ListGroupsIqProtocolEntity, self).__init__(to = "g.us", _type = "get", _id = _id)
        self.setProps(groupsType)

    def setProps(self, groupsType):
        assert groupsType in self.__class__.GROUPS_TYPES,\
            "Groups type must be %s, not %s" % (" or ".join(self.__class__.GROUPS_TYPES), groupsType)
        self.groupsType = groupsType

    def toProtocolTreeNode(self):
        node = super(ListGroupsIqProtocolEntity, self).getProtocolTreeNode("w:g")
        node.addChild(ProtocolTreeNode("list",{"type": self.groupsType}, ns="w:g"))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ListGroupsIqProtocolEntity(node.getChild("list").getAttributeValue("type"), _id=node["id"])
        return entity