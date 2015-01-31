from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class DeleteGroupsIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_groups_delete.xsd")
    '''
    <iq id="{{id}}"" type="set" to="{{group_jid}}" xmlns="w:g">
        <group action="delete"></group>
    </iq>
    '''

    def __init__(self, groupJid, _id = None):
        super(DeleteGroupsIqProtocolEntity, self).__init__(to = groupJid, _type = "set", _id = _id)
        self.setProps(groupJid)

    def setProps(self, groupJid):
        self.groupJid = groupJid

    def toProtocolTreeNode(self):
        node = super(DeleteGroupsIqProtocolEntity, self).getProtocolTreeNode("w:g")
        node.addChild(ProtocolTreeNode("group", {"action": "delete"}, ns="w:g"))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DeleteGroupsIqProtocolEntity(node["to"], _id = node["id"])
        return entity