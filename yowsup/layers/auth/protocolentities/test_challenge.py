from yowsup.layers.auth.protocolentities.challenge import ChallengeProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class ChallengeProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ChallengeProtocolEntity
        self.xml = "<challenge>challenge_data</challenge>"