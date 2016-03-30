from yowsup.common import YowConstants
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class SuccessCreateGroupsIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" id="{{id}}" from="g.us">
        <group id="{group_id}"></group>
    </iq>
    '''

    def __init__(self, _id, groupId):
        super(SuccessCreateGroupsIqProtocolEntity, self).__init__(_from = YowConstants.WHATSAPP_GROUP_SERVER, _id = _id)
        self.setProps(groupId)

    def setProps(self, groupId):
        self.groupId = groupId

    def toProtocolTreeNode(self):
        node = super(SuccessCreateGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("group",{"id": self.groupId}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(SuccessCreateGroupsIqProtocolEntity, SuccessCreateGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = SuccessCreateGroupsIqProtocolEntity
        entity.setProps(node.getChild("group").getAttributeValue("id"))
        return entity
