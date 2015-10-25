from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import GetPrivacyIqProtocolEntity
from yowsup.structs import ProtocolTreeNode

entity = GetPrivacyIqProtocolEntity()

class GetPrivacyIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(GetPrivacyIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = GetPrivacyIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
