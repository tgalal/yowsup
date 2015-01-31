from yowsup.layers.protocol_iq.protocolentities.iq import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class IqProtocolEntityTest(unittest.TestCase, ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = IqProtocolEntity
        self.node = ProtocolTreeNode("iq", {"id": "iq_iid", "type": "get", "to": "to"}, None, None)
        self.xml = """
            <iq type="get" id="iq_iid"  to="to" />
            """