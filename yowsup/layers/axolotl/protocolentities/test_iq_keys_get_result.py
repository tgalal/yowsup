from yowsup.layers.protocol_iq.protocolentities.test_iq_result import ResultIqProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import ResultGetKeysIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from axolotl.util.keyhelper import KeyHelper
from axolotl.ecc.curve import Curve

class ResultGetKeysIqProtocolEntityTest(ResultIqProtocolEntityTest):
    def setUp(self):
        super(ResultIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ResultGetKeysIqProtocolEntity
        self.xml = """
            <iq type="result" from="s.whatsapp.net" id="3">
                <list>
                    <user jid="79049347231@s.whatsapp.net">
                        <registration>123456</registration>
                        <type>5</type>
                        <identity>eeb668c8d062c99b43560c811acfe6e492798b496767eb060d99e011d3862369</identity>
                        <skey>
                            <id>000000</id>
                            <value>a1b5216ce4678143fb20aaaa2711a8c2b647230164b79414f0550b4e611ccd6c</value>
                            <signature>SIG HERE</signature>
                        </skey>
                        <key>
                            <id>36b545</id>
                            <value>c20826f622bec24b349ced38f1854bdec89ba098ef4c06b2402800d33e9aff61</value>
                        </key>
                    </user>
                </list>
            </iq>
        """

        # listNode = ProtocolTreeNode("list")
        # self.node.addChild(listNode)
        #
        # for i in range(0, 1):
        #     userNode = ProtocolTreeNode("user", {"jid": "user_%s@s.whatsapp.net" % i})
        #     listNode.addChild(userNode)
        #     registrationNode = ProtocolTreeNode("registration",
        #                                         data = ResultGetKeysIqProtocolEntity._intToBytes(
        #                                             KeyHelper.generateRegistrationId()))
        #
        #     typeNode = ProtocolTreeNode("type", data = ResultGetKeysIqProtocolEntity._intToBytes(Curve.DJB_TYPE))
        #
        #     identityKeyPair = KeyHelper.generateIdentityKeyPair()
        #     identityNode = ProtocolTreeNode("identity", data=identityKeyPair.getPublicKey().getPublicKey().getPublicKey())
        #
        #     signedPreKey = KeyHelper.generateSignedPreKey(identityKeyPair, i)
        #
        #     signedPreKeyNode = ProtocolTreeNode("skey")
        #     signedPreKeyNode_idNode = ProtocolTreeNode("id",
        #                                                data = ResultGetKeysIqProtocolEntity._intToBytes(
        #                                                    signedPreKey.getId()))
        #
        #     signedPreKeyNode_valueNode = ProtocolTreeNode("value",
        #                                                   data = signedPreKey.getKeyPair().getPublicKey().getPublicKey())
        #
        #     signedPreKeyNode_sigNode = ProtocolTreeNode("signature",
        #                                                 data = signedPreKey.getSignature())
        #
        #     signedPreKeyNode.addChildren([signedPreKeyNode_idNode, signedPreKeyNode_valueNode, signedPreKeyNode_sigNode])
        #
        #     preKey = KeyHelper.generatePreKeys(i * 10, 1)[0]
        #
        #     preKeyNode = ProtocolTreeNode("key")
        #     preKeyNode_idNode = ProtocolTreeNode("id", data = ResultGetKeysIqProtocolEntity._intToBytes(preKey.getId()))
        #     preKeyNode_valNode = ProtocolTreeNode("value", data = preKey.getKeyPair().getPublicKey().getPublicKey())
        #     preKeyNode.addChildren([preKeyNode_idNode, preKeyNode_valNode])
        #
        #     userNode.addChildren([
        #         registrationNode,
        #         typeNode,
        #         identityNode,
        #         signedPreKeyNode,
        #         preKeyNode
        #     ])


