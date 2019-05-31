from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from axolotl.state.prekeybundle import PreKeyBundle
from axolotl.identitykey import IdentityKey
from axolotl.ecc.curve import Curve
from axolotl.ecc.djbec import DjbECPublicKey
import binascii
import sys


class ResultGetKeysIqProtocolEntity(ResultIqProtocolEntity):
    """
    <iq type="result" from="s.whatsapp.net" id="3">
    <list>
    <user jid="79049347231@s.whatsapp.net">
    <registration>
        HEX:7a9cec4b</registration>
    <type>

    HEX:05</type>
    <identity>
    HEX:eeb668c8d062c99b43560c811acfe6e492798b496767eb060d99e011d3862369</identity>
    <skey>
    <id>

    HEX:000000</id>
    <value>
    HEX:a1b5216ce4678143fb20aaaa2711a8c2b647230164b79414f0550b4e611ccd6c</value>
    <signature>
    HEX:94c231327fcd664b34603838b5e9ba926718d71c206e92b2b400f5cf4ae7bf17d83557bf328c1be6d51efdbd731a26d000adb8f38f140b1ea2a5fd3df2688085</signature>
        </skey>
    <key>
        <id>
        HEX:36b545</id>
    <value>
    HEX:c20826f622bec24b349ced38f1854bdec89ba098ef4c06b2402800d33e9aff61</value>
    </key>
    </user>
    </list>
    </iq>
    """
    def __init__(self, _id, preKeyBundleMap = None):
        super(ResultGetKeysIqProtocolEntity, self).__init__(_from = YowConstants.WHATSAPP_SERVER, _id=_id)
        self.setPreKeyBundleMap(preKeyBundleMap)
        self._errors = {}

    def getJids(self):
        return self.preKeyBundleMap.keys()

    def getErrors(self):
        return self._errors.copy()

    def setErrorFor(self, jid, exception):
        self._errors[jid] = exception

    def setPreKeyBundleMap(self, preKeyBundleMap = None):
        self.preKeyBundleMap = preKeyBundleMap or {}

    def setPreKeyBundleFor(self, jid, preKeyBundle):
        self.preKeyBundleMap[jid] = preKeyBundle

    def getPreKeyBundleFor(self, jid):
        if jid in self.preKeyBundleMap:
            return self.preKeyBundleMap[jid]

    @staticmethod
    def _intToBytes(val):
        return binascii.unhexlify(format(val, 'x').zfill(8).encode())

    @staticmethod
    def _bytesToInt(val):
        if sys.version_info >= (3,0):
            valEnc = val.encode('latin-1') if type(val) is str else val
        else:
            valEnc = val
        return int(binascii.hexlify(valEnc), 16)

    @staticmethod
    def encStr(string):
        if sys.version_info >= (3,0) and type(string) is str:
            return string.encode('latin-1')
        return string

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ResultGetKeysIqProtocolEntity(node["id"])
        userNodes = node.getChild("list").getAllChildren()
        for userNode in userNodes:
            missing_params = []
            preKeyNode = userNode.getChild("key")
            signedPreKeyNode = userNode.getChild("skey")
            registrationNode = userNode.getChild("registration")
            identityNode = userNode.getChild("identity")

            if preKeyNode is None:
                missing_params.append(MissingParametersException.PARAM_KEY)
            if signedPreKeyNode is None:
                missing_params.append(MissingParametersException.PARAM_SKEY)
            if registrationNode is None:
                missing_params.append(MissingParametersException.PARAM_REGISTRATION)
            if identityNode is None:
                missing_params.append(MissingParametersException.PARAM_IDENTITY)

            if len(missing_params):
                entity.setErrorFor(userNode["jid"], MissingParametersException(userNode["jid"], missing_params))
            else:
                registrationId = ResultGetKeysIqProtocolEntity._bytesToInt(registrationNode.getData())
                identityKey = IdentityKey(DjbECPublicKey(ResultGetKeysIqProtocolEntity.encStr(identityNode.getData())))

                preKeyId = ResultGetKeysIqProtocolEntity._bytesToInt(preKeyNode.getChild("id").getData())
                preKeyPublic = DjbECPublicKey(ResultGetKeysIqProtocolEntity.encStr(preKeyNode.getChild("value").getData()))

                signedPreKeyId = ResultGetKeysIqProtocolEntity._bytesToInt(signedPreKeyNode.getChild("id").getData())
                signedPreKeySig = ResultGetKeysIqProtocolEntity.encStr(signedPreKeyNode.getChild("signature").getData())
                signedPreKeyPub = DjbECPublicKey(ResultGetKeysIqProtocolEntity.encStr(signedPreKeyNode.getChild("value").getData()))

                preKeyBundle = PreKeyBundle(registrationId, 1, preKeyId, preKeyPublic,
                                            signedPreKeyId, signedPreKeyPub, signedPreKeySig, identityKey)

                entity.setPreKeyBundleFor(userNode["jid"], preKeyBundle)

        return entity

    def toProtocolTreeNode(self):
        node = super(ResultGetKeysIqProtocolEntity, self).toProtocolTreeNode()
        listNode = ProtocolTreeNode("list")
        node.addChild(listNode)

        for jid, preKeyBundle in self.preKeyBundleMap.items():
            userNode = ProtocolTreeNode("user", {"jid": jid})
            registrationNode = ProtocolTreeNode("registration", data = self.__class__._intToBytes(preKeyBundle.getRegistrationId()))
            typeNode = ProtocolTreeNode("type", data = self.__class__._intToBytes(Curve.DJB_TYPE))
            identityNode = ProtocolTreeNode("identity", data = preKeyBundle.getIdentityKey().getPublicKey().getPublicKey())

            skeyNode = ProtocolTreeNode("skey")
            skeyNode_idNode = ProtocolTreeNode("id", data=self.__class__._intToBytes(preKeyBundle.getSignedPreKeyId()))
            skeyNode_valueNode = ProtocolTreeNode("value", data=preKeyBundle.getSignedPreKey().getPublicKey())
            skeyNode_signatureNode = ProtocolTreeNode("signature", data=preKeyBundle.getSignedPreKeySignature())
            skeyNode.addChildren([skeyNode_idNode, skeyNode_valueNode, skeyNode_signatureNode])

            preKeyNode = ProtocolTreeNode("key")
            preKeyNode_idNode = ProtocolTreeNode("id", data = self.__class__._intToBytes(preKeyBundle.getPreKeyId()))
            preKeyNode_valueNode = ProtocolTreeNode("value", data= preKeyBundle.getPreKey().getPublicKey())
            preKeyNode.addChildren([preKeyNode_idNode, preKeyNode_valueNode])

            userNode.addChildren([
                registrationNode,
                typeNode,
                identityNode,
                skeyNode,
                preKeyNode
            ])
            listNode.addChild(userNode)

        return node


class MissingParametersException(Exception):
    PARAM_KEY = "key"
    PARAM_IDENTITY = "identity"
    PARAM_SKEY = "skey"
    PARAM_REGISTRATION = "registration"
    __PARAMS = (PARAM_KEY, PARAM_IDENTITY, PARAM_SKEY, PARAM_REGISTRATION)

    def __init__(self, jid, parameters):
        # type: (str, list | str) -> None
        self._jid = jid
        assert type(parameters) in (list, str)
        if type(parameters) is str:
            parameters = list(parameters)
        assert len(parameters) > 0
        for p in parameters:
            assert p in self.__PARAMS, "%s is unrecognized param" % p

        self._parameters = parameters

    @property
    def jid(self):
        return self._jid

    @property
    def parameters(self):
        return self._parameters
