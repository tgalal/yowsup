from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
import sys
from yowsup.layers.axolotl.protocolentities.enc import EncProtocolEntity
class EncryptedMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message retry="1" from="49xxxxxxxx@s.whatsapp.net" t="1418906418" offline="1" type="text" id="1418906377-1" notify="Tarek Galal">
<enc type="{{type}}" v="{{1 || 2}}">
HEX:33089eb3c90312210510e0196be72fe65913c6a84e75a54f40a3ee290574d6a23f408df990e718da761a210521f1a3f3d5cb87fde19fadf618d3001b64941715efd3e0f36bba48c23b08c82f2242330a21059b0ce2c4720ec79719ba862ee3cda6d6332746d05689af13aabf43ea1c8d747f100018002210d31cd6ebea79e441c4935f72398c772e2ee21447eb675cfa28b99de8d2013000</enc>
</message>

<message from="49xxxxxxx@s.whatsapp.net" notify="Tarek Galal" offline="1" type="media" id="D6D2D11814171B93A435D45A1234C" t="1458776105">
<enc type="pkmsg" mediatype="image" v="2">
HEX:33089eb3c90312210510e0196be72fe65913c6a84e75a54f40a3ee290574d6a23f408df990e718da761a210521f1a3f3d5cb87fde19fadf618d3001b64941715efd3e0f36bba48c23b08c82f2242330a21059b0ce2c4720ec79719ba862ee3cda6d6332746d05689af13aabf43ea1c8d747f100018002210d31cd6ebea79e441c4935f72398c772e2ee21447eb675cfa28b99de8d2013000</enc>
</message>

    '''

    def __init__(self, encEntities, _type, _id = None,  _from = None, to = None, notify = None, timestamp = None,
            participant = None, offline = None, retry = None ):
        super(EncryptedMessageProtocolEntity, self).__init__(_type, _id = _id,  _from = _from, to = to, notify = notify,
                                                      timestamp = timestamp, participant = participant, offline = offline,
                                                      retry = retry)
        self.setEncEntities(encEntities)

    def setEncEntities(self, encEntities):
        assert len(encEntities), "Must have at least 1 enc entity"
        self.encEntities = encEntities

    def getEnc(self, encType):
        for enc in self.encEntities:
            if enc.type == encType:
                return enc

    def toProtocolTreeNode(self):
        node = super(EncryptedMessageProtocolEntity, self).toProtocolTreeNode()
        participantsNode = ProtocolTreeNode("participants")
        for enc in self.encEntities:
            encNode = enc.toProtocolTreeNode()
            if encNode.tag == "to":
                participantsNode.addChild(encNode)
            else:
                node.addChild(encNode)

        if len(participantsNode.getAllChildren()):
            node.addChild(participantsNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = EncryptedMessageProtocolEntity
        entity.setEncEntities([EncProtocolEntity.fromProtocolTreeNode(encNode) for encNode in node.getAllChildren("enc")])
        return entity
