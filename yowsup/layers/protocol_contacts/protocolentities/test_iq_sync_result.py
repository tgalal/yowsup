from yowsup.layers.protocol_contacts.protocolentities.iq_sync_result import ResultSyncIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
from lxml import etree

entity = ResultSyncIqProtocolEntity("123", "1.30615237617e+17", 0,
                                            True, "123456", {"12345678": "12345678@s.whatsapp.net"},
                                            {"12345678": "12345678@s.whatsapp.net"}, ["1234"])

class ResultSyncIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ResultSyncIqProtocolEntity
        self.xml = entity.toProtocolTreeNode().__str__()
