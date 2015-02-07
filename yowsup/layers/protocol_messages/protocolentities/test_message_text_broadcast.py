from yowsup.layers.protocol_messages.protocolentities.message_text_broadcast import BroadcastTextMessage
import unittest
from yowsup.structs.protocolentity import ProtocolEntityTest
class BroadcastTextMessageTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = BroadcastTextMessage
        self.xml = """
        <message to="1422936169039@broadcast" type="text" id="1422936169-1">
            <body>HELLO</body>
            <broadcast>
                <to jid="491632092557@s.whatsapp.net" />
            </broadcast>
        </message>
        """
