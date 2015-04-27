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
            __init__(_from="g.us", _id=_id)
        self.setProps(groupId)

    def setProps(self, groupId):
        self.groupId = groupId

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
        entity = ResultIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SuccessLeaveGroupsIqProtocolEntity
        entity.setProps(
            node.getChild("leave").getChild("group").getAttributeValue("id")
        )
        return entity
