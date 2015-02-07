from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
import unittest
from yowsup.structs.protocolentity import ProtocolEntityTest

class TextMessageProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        super(TextMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = TextMessageProtocolEntity
        self.xml="""
        <message retry="4" participant="201000046084@s.whatsapp.net" t="1422801610" notify="Ahmed ElMahdy" from="201222980047-1330796006@g.us" offline="4" type="text" id="1422739247-41" phash="1:pqIhDPHe">
            <body>aaaa</body>
        </message>
        """
