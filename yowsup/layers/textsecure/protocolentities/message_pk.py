from yowsup.layers.protocol_messages.protocolentities import MessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
class PkMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message retry="1" from="4917675341470@s.whatsapp.net" t="1418906418" offline="1" type="text" id="1418906377-1" notify="Tarek Galal">
<enc av="Android/2.11.456" type="pkmsg" v="1">
HEX:33089eb3c90312210510e0196be72fe65913c6a84e75a54f40a3ee290574d6a23f408df990e718da761a210521f1a3f3d5cb87fde19fadf618d3001b64941715efd3e0f36bba48c23b08c82f2242330a21059b0ce2c4720ec79719ba862ee3cda6d6332746d05689af13aabf43ea1c8d747f100018002210d31cd6ebea79e441c4935f72398c772e2ee21447eb675cfa28b99de8d2013000</enc>
</message>
    '''

    def __init__(self, encType, encAv, encVersion, encData, _type, _id = None,  _from = None, to = None, notify = None, timestamp = None,
            participant = None, offline = None, retry = None ):
        super(PkMessageProtocolEntity, self).__init__(_type, _id = None,  _from = None, to = None, notify = None,
                                                      timestamp = None, participant = None, offline = None,
                                                      retry = None)

        self.setEncProps(encType, encAv, encVersion, encData)

    def setEncProps(self, encType, encAv, encVersion, encData):
        assert encType == "pkmsg", "Only pkmsg is implemented for now"
        self.encType = encType
        self.encAv = encAv
        self.encVersion = encVersion
        self.encData = encData

        self.prewhispermessage = PreKeyWhisperMessage(serialized= bytearray(encData))

        #self.registrationId = preKeyWhisperMessage.registrationId
        #self.pkId = preKeyWhisperMessage.preKeyId

    def getEncType(self):
        return self.encType

    def getEncAv(self):
        return self.encAv

    def getEncData(self):
        return self.encData

    def getPkVersion(self):
        return self.prewhispermessage.version

    def getPkRegistrationId(self):
        return self.prewhispermessage.registrationId

    def getPkId(self):
        return self.prewhispermessage.preKeyId

    def getPkBaseKey(self):
        return self.prewhispermessage.baseKey

    def getPkIdentity(self):
        return self.prewhispermessage.identityKey

    def getPkMessage(self):
        return self.prewhispermessage

    def getPkCipherMessage(self):
        return self.prewhispermessage.message


    def toProtocolTreeNode(self):
        node = super(PkMessageProtocolEntity, self).toProtocolTreeNode()
        encNode = ProtocolTreeNode("enc", data = self.encData)
        encNode["type"] = self.encType
        encNode["av"] = self.encAv
        encNode["v"] = self.encVersion

        node.addChild(encNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = PkMessageProtocolEntity
        encNode = node.getChild("enc")
        entity.setEncProps(encNode["type"], encNode["av"], encNode["v"], encNode.data)
        return entity