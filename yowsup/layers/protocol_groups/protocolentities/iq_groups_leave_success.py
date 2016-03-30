from yowsup.common import YowConstants
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity


class SuccessLeaveGroupsIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" from="g.us" id="{{ID}}">
        <leave>
            <group id="{{GROUP_JID}}"></group>
        </leave>
    </iq>
    '''

    def __init__(self, _id, groupId):
        super(SuccessLeaveGroupsIqProtocolEntity, self).\
            __init__(_from=YowConstants.WHATSAPP_GROUP_SERVER, _id=_id)
        self.setProps(groupId)

    def setProps(self, groupId):
        self.groupId = groupId

    def __str__(self):
        out = super(SuccessLeaveGroupsIqProtocolEntity, self).__str__()
        out += "Group Id: %s\n" % self.groupId
        return out

    def toProtocolTreeNode(self):
        node = super(SuccessLeaveGroupsIqProtocolEntity, self).\
            toProtocolTreeNode()
        leaveNode = ProtocolTreeNode(
            "leave", {}, [ProtocolTreeNode("group", {"id": self.groupId})]
        )
        node.addChild(leaveNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(SuccessLeaveGroupsIqProtocolEntity, SuccessLeaveGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = SuccessLeaveGroupsIqProtocolEntity
        entity.setProps(
            node.getChild("leave").getChild("group").getAttributeValue("id")
        )
        return entity
