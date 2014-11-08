from Yowsup.layers.auth import YowAuthenticatorLayer
from Yowsup.layers import YowLayerEvent, YowLayerTest
from Yowsup.layers.auth.protocolentities import StreamFeaturesProtocolEntity,AuthProtocolEntity, ChallengeProtocolEntity
from Yowsup.structs import ProtocolTreeNode
import base64
# from unittest.mock import MagicMock


class AuthenticatorLayerTest(YowLayerTest, YowAuthenticatorLayer):
    def setUp(self):
        YowAuthenticatorLayer.__init__(self)
        self.credentials =  ("dummyusername", bytearray("passwordpassword", "latin-1"))
        YowAuthenticatorLayer.setProp("credentials", self.credentials)

    def test_streamfeatures(self):
        self._sendFeatures()
        self.assertEqual(self.dataSink.toString(), StreamFeaturesProtocolEntity().toProtocolTreeNode().toString())

    def test_auth(self):
        self._sendAuth()
        self.assertEqual(self.dataSink.toString(), AuthProtocolEntity(self.credentials[0]).toProtocolTreeNode().toString())

    def test_handle_challenge(self):
        node = ProtocolTreeNode("challenge", {}, None, "salt")
        self.handleChallenge(node)



    def test_login_onconnected(self):
        self.onEvent(YowLayerEvent("network.state.connected"))
