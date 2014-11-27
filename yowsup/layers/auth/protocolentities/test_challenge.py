from yowsup.layers.auth.protocolentities.challenge import ChallengeProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class ChallengeProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = ChallengeProtocolEntity
        attribs             = {}
        childNodes          = []
        data                = "dummydata"
        self.node = ProtocolTreeNode("challenge", attribs, [], data)