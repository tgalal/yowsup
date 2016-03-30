from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
import os, time
class SetKeysIqProtocolEntity(IqProtocolEntity):
    def __init__(self, identityKey, signedPreKey, preKeys, djbType, registrationId = None):
        super(SetKeysIqProtocolEntity, self).__init__("encrypt", _type = "set", to = YowConstants.WHATSAPP_SERVER)
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
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SetKeysIqProtocolEntity
        regVal = node.getChild("registration").data
        typeVal = node.getChild("type").data
        idVal = node.getChild("identity").data

        preKeys = {}
        for keyNode in node.getChild("list").getAllChildren():
            preKeys[keyNode.getChild("id").data] = keyNode.getChild("value").data


        skeyNode = node.getChild("skey")
        entity.setProps(idVal, (skeyNode.getChild("id").data, skeyNode.getChild("value").data,
                                skeyNode.getChild("signature").data), preKeys, typeVal, regVal)

        return entity

    def toProtocolTreeNode(self):
        node = super(SetKeysIqProtocolEntity, self).toProtocolTreeNode()
        identityNode = ProtocolTreeNode("identity", data = self.identityKey)

        listNode = ProtocolTreeNode("list")
        keyNodes = []
        for keyId, pk in self.preKeys.items():
            keyNode = ProtocolTreeNode("key")
            keyNode.addChild(ProtocolTreeNode("id", data = keyId))
            keyNode.addChild(ProtocolTreeNode("value", data = pk))
            keyNodes.append(keyNode)

        listNode.addChildren(keyNodes)

        regNode = ProtocolTreeNode("registration", data = self.registration)
        typeNode = ProtocolTreeNode("type", data = chr(self.djbType))
        _id, val, signature = self.signedPreKey
        skeyNode = ProtocolTreeNode("skey", children = [
            ProtocolTreeNode("id", data = _id),
            ProtocolTreeNode("value", data = val),
            ProtocolTreeNode("signature", data = signature)
        ])

        node.addChildren([
            listNode,
            identityNode,
            regNode,
            typeNode,
            skeyNode
        ])

        return node
