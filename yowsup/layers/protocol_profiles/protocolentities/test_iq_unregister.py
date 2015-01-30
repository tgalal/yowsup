from yowsup.structs.protocolentity import ProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import UnregisterIqProtocolEntity
import unittest

class UnregisterIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        super(UnregisterIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnregisterIqProtocolEntity
        self.xml = """
            <iq id="1234" type="get" to="s.whatsapp.net">
                <remove xmlns="urn:xmpp:whatsapp:account" />
            </iq>
        """