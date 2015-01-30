from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import UnregisterIqProtocolEntity

class UnregisterIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(UnregisterIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnregisterIqProtocolEntity
        self.xml = """
            <iq id="1234" type="get" to="s.whatsapp.net">
                <remove xmlns="urn:xmpp:whatsapp:account" />
            </iq>
        """