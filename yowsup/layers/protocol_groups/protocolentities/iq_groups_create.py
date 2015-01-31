from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class CreateGroupsIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_groups_create.xsd")
    '''
    <iq type="set" id="{{id}}" xmlns="w:g" to="g.us">
        <group action="create" subject="{{subject}}"></group>
    </iq>
    '''

    def __init__(self, subject, _id = None):
        super(CreateGroupsIqProtocolEntity, self).__init__(to = "g.us", _id = _id, _type = "set")
        self.setProps(subject)

    def setProps(self, subject):
        self.subject = subject

    def toProtocolTreeNode(self):
        node = super(CreateGroupsIqProtocolEntity, self).getProtocolTreeNode("w:g")
        node.addChild(ProtocolTreeNode("group",{"action": "create", "subject": self.subject}, ns="w:g"))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        return CreateGroupsIqProtocolEntity(node.getChild("group").getAttributeValue("subject"), _id = node["id"])
