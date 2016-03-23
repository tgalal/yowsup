from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class SetStatusIqProtocolEntity(IqProtocolEntity):
    '''
    <iq to="s.whatsapp.net" xmlns="status" type="set" id="{{IQ_ID}}">
        <status>{{MSG}}</status>
    </notification>
    '''
    XMLNS = "status"
    def __init__(self, text = None, _id = None):
        super(SetStatusIqProtocolEntity, self).__init__(self.__class__.XMLNS, _id, _type = "set", to = YowConstants.WHATSAPP_SERVER)
        self.setData(text)
        
    def setData(self, text):
        self.text = text

    def toProtocolTreeNode(self):
        node = super(SetStatusIqProtocolEntity, self).toProtocolTreeNode()
        statusNode = ProtocolTreeNode("status", {}, [], self.text)
        node.addChild(statusNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SetStatusIqProtocolEntity
        statusNode = node.getChild("status")
        entity.setData(statusNode.getData())
        return entity
