from yowsup.layers.protocol_contacts.protocolentities.iq_sync_result import ResultSyncIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

entity = ResultSyncIqProtocolEntity("123", "1.30615237617e+17", 0,
                                            True, "123456", {"12345678": "12345678@s.whatsapp.net"},
                                            {"12345678": "12345678@s.whatsapp.net"}, ["1234"])

class ResultSyncIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ResultSyncIqProtocolEntity
        self.node = entity.toProtocolTreeNode()

    def test_delta_result(self):
        del self.node.getChild("sync")["wait"]
        self.test_generation()
