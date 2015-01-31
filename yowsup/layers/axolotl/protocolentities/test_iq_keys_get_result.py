from yowsup.layers.axolotl.protocolentities import ResultGetKeysIqProtocolEntity
import unittest
from yowsup.structs.protocolentity import ProtocolEntityTest
class ResultGetKeysIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
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

