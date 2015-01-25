from yowsup.layers.auth.protocolentities.success import SuccessProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class SuccessProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = SuccessProtocolEntity
        self.xml = '<success status="active" kind="free" creation="123456789" expiration="987654321" props="4" t="12121212">aaaaaa</success>'