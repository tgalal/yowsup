from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import SetPrivacyIqProtocolEntity
from yowsup.structs import ProtocolTreeNode

entity = SetPrivacyIqProtocolEntity("all", ["profile","last","status"])

class SetPrivacyIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(SetPrivacyIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SetPrivacyIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
