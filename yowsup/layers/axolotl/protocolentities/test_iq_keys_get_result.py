from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities.test_iq_result import ResultIqProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import ResultGetKeysIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from axolotl.util.keyhelper import KeyHelper
from axolotl.ecc.curve import Curve

class ResultGetKeysIqProtocolEntityTest(ResultIqProtocolEntityTest):
    def setUp(self):
        super(ResultIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ResultGetKeysIqProtocolEntity
        listNode = ProtocolTreeNode("list")
        self.node.addChild(listNode)

        for i in range(0, 1):
            userNode = ProtocolTreeNode("user", {"jid": "user_%s@%s" % (i, YowConstants.WHATSAPP_SERVER)})
            listNode.addChild(userNode)
            registrationNode = ProtocolTreeNode("registration",
                                                data = ResultGetKeysIqProtocolEntity._intToBytes(
                                                    KeyHelper.generateRegistrationId()))

            typeNode = ProtocolTreeNode("type", data = ResultGetKeysIqProtocolEntity._intToBytes(Curve.DJB_TYPE))

            identityKeyPair = KeyHelper.generateIdentityKeyPair()
            identityNode = ProtocolTreeNode("identity", data=identityKeyPair.getPublicKey().getPublicKey().getPublicKey())

            signedPreKey = KeyHelper.generateSignedPreKey(identityKeyPair, i)

            signedPreKeyNode = ProtocolTreeNode("skey")
            signedPreKeyNode_idNode = ProtocolTreeNode("id",
                                                       data = ResultGetKeysIqProtocolEntity._intToBytes(
                                                           signedPreKey.getId()))

            signedPreKeyNode_valueNode = ProtocolTreeNode("value",
                                                          data = signedPreKey.getKeyPair().getPublicKey().getPublicKey())

            signedPreKeyNode_sigNode = ProtocolTreeNode("signature",
                                                        data = signedPreKey.getSignature())

            signedPreKeyNode.addChildren([signedPreKeyNode_idNode, signedPreKeyNode_valueNode, signedPreKeyNode_sigNode])

            preKey = KeyHelper.generatePreKeys(i * 10, 1)[0]

            preKeyNode = ProtocolTreeNode("key")
            preKeyNode_idNode = ProtocolTreeNode("id", data = ResultGetKeysIqProtocolEntity._intToBytes(preKey.getId()))
            preKeyNode_valNode = ProtocolTreeNode("value", data = preKey.getKeyPair().getPublicKey().getPublicKey())
            preKeyNode.addChildren([preKeyNode_idNode, preKeyNode_valNode])

            userNode.addChildren([
                registrationNode,
                typeNode,
                identityNode,
                signedPreKeyNode,
                preKeyNode
            ])

