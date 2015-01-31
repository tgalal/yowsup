from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
import os
class SetKeysIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_keys_set.xsd")
    def __init__(self, identityKey, signedPreKey, preKeys, djbType, registrationId = None, _id = None):
        super(SetKeysIqProtocolEntity, self).__init__( _type = "set", to = "s.whatsapp.net", _id = _id)
        self.setProps(identityKey, signedPreKey, preKeys, djbType, registrationId)

    def setProps(self, identityKey, signedPreKey, preKeys, djbType, registrationId = None):
        assert type(preKeys) is dict, "Expected keys to be a dict key_id -> public_key"
        assert type(signedPreKey) is tuple, "Exception signed pre key to be tuple id,key,signature"
        self.preKeys = preKeys
        self.identityKey = identityKey
        self.registration = registrationId or os.urandom(4)
        self.djbType = int(djbType)
        self.signedPreKey = signedPreKey

    @staticmethod
    def fromProtocolTreeNode(node):
        regVal = node.getChild("registration").getData()
        typeVal = ord(node.getChild("type").getData())
        idVal = node.getChild("identity").getData()

        preKeys = {}
        for keyNode in node.getChild("list").getAllChildren():
            preKeys[keyNode.getChild("id").getData()] = keyNode.getChild("value").getData()


        skeyNode = node.getChild("skey")


        entity = SetKeysIqProtocolEntity(idVal, (skeyNode.getChild("id").getData(), skeyNode.getChild("value").getData(),
                                skeyNode.getChild("signature").getData()), preKeys, typeVal, regVal, _id=node["id"])

        return entity

    def toProtocolTreeNode(self):
        node = super(SetKeysIqProtocolEntity, self).getProtocolTreeNode("encrypt")
        ProtocolTreeNode("identity", data = self.identityKey, parent=node)

        listNode = ProtocolTreeNode("list", parent=node)
        for keyId, pk in self.preKeys.items():
            keyNode = ProtocolTreeNode("key", parent=listNode)
            ProtocolTreeNode("id", data = keyId, parent=keyNode)
            ProtocolTreeNode("value", data = pk, parent=keyNode)


        ProtocolTreeNode("registration", data = self.registration, parent=node)
        ProtocolTreeNode("type", data = chr(self.djbType), parent=node)
        _id, val, signature = self.signedPreKey


        skeyNode = ProtocolTreeNode("skey", parent=node)
        ProtocolTreeNode("id", data = _id, parent=skeyNode),
        ProtocolTreeNode("value", data = val, parent=skeyNode),
        ProtocolTreeNode("signature", data = signature, parent=skeyNode)


        return node