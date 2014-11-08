from .challenge import ChallengeProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class ChallengeProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = ChallengeProtocolEntity
        attribs             = {}
        childNodes          = []
        data                = "dummydata"
        self.node = ProtocolTreeNode("challenge", attribs, [], data)