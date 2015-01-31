from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import SetKeysIqProtocolEntity
class SetKeysIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = SetKeysIqProtocolEntity
        self.xml = """
             <iq type="set" xmlns="encrypt" to="s.whatsapp.net" id="3">
                <registration  meta-yowsup-encoding="hex">123456</registration>
                <type meta-yowsup-encoding="hex">05</type>
                <identity>eeb668c8d062c99b43560c811acfe6e492798b496767eb060d99e011d3862369</identity>
                <skey>
                    <id meta-yowsup-encoding="hex">000000</id>
                    <value meta-yowsup-encoding="hex">a1b5216ce4678143fb20aaaa2711a8c2b647230164b79414f0550b4e611ccd6c</value>
                    <signature meta-yowsup-encoding="hex">0000</signature>
                </skey>
                <list>
                    <key>
                        <id meta-yowsup-encoding="hex">36b545</id>
                        <value meta-yowsup-encoding="hex">c20826f622bec24b349ced38f1854bdec89ba098ef4c06b2402800d33e9aff61</value>
                    </key>
                    <key>
                        <id meta-yowsup-encoding="hex">36b545</id>
                        <value meta-yowsup-encoding="hex">c20826f622bec24b349ced38f1854bdec89ba098ef4c06b2402800d33e9aff61</value>
                    </key>

                </list>
            </iq>
        """
