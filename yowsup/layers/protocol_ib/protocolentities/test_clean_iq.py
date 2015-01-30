from yowsup.layers.protocol_ib.protocolentities.clean_iq import CleanIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class CleanIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = CleanIqProtocolEntity
        self.xml = """
            <iq id="1" type="set" to="s.whatsapp.net" xmlns="urn:xmpp:whatsapp:dirty">
                <clean type="type_ditty"></clean>
            </iq>
        """