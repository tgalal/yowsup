from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from .dec import DecProtocolEntity
class DecryptedMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message retry="1" from="49xxxxxxxx@s.whatsapp.net" t="1418906418" offline="1" type="text" id="1418906377-1" notify="Tarek Galal">
<dec mediatype="image|audio|location|document|contact ...">
    protobuf data
</dec
</message>
    '''

    def __init__(self, decEntity, _type, _id = None,  _from = None, to = None, notify = None, timestamp = None,
            participant = None, offline = None, retry = None):
        super(DecryptedMessageProtocolEntity, self).__init__(_type, _id = _id,  _from = _from, to = to, notify = notify,
                                                      timestamp = timestamp, participant = participant, offline = offline,
                                                      retry = retry)
        self.setDecEntities(decEntity)

    def setDecEntity(self, decEntity):
        self.decEntity = decEntity

    def getDec(self):
        return self.decEntity

    def toProtocolTreeNode(self):
        node = super(DecryptedMessageProtocolEntity, self).toProtocolTreeNode()
        node.addChild(self.decEntity.toProtocolTreeNode())

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DecryptedMessageProtocolEntity
        decNode = node.getChild("dec")
        assert decNode is not None
        entity.setDecEntity(
            DecProtocolEntity.fromProtocolTreeNode(decNode)
        )
        return entity
