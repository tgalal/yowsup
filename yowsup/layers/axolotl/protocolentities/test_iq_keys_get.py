from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
from yowsup.layers.axolotl.protocolentities import GetKeysIqProtocolEntity

class GetKeysIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = GetKeysIqProtocolEntity
        self.xml = """
            <iq xmlns="encrypt" to="s.whatsapp.net" type="get" id="2">
                <key>
                    <user jid="aaa@s.whatsapp.net"/>
                    <user jid="bbb@s.whatsapp.net"/>
                </key>
            </iq>
            """

        self.node = GetKeysIqProtocolEntity(["aaa@s.whatsapp.net", "bbb@s.whatsapp.net"], "2").toProtocolTreeNode()