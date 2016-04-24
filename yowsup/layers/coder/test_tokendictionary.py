from yowsup.layers.coder.tokendictionary import TokenDictionary
import unittest
class TokenDictionaryTest(unittest.TestCase):
    def setUp(self):
        self.tokenDictionary = TokenDictionary()

    def test_getToken(self):
        self.assertEqual(self.tokenDictionary.getToken(80), "iq")

    def test_getIndex(self):
        self.assertEqual(self.tokenDictionary.getIndex("iq"), (80, False))

    def test_getSecondaryToken(self):
        self.assertEqual(self.tokenDictionary.getToken(238), "amrnb")

    def test_getSecondaryTokenExplicit(self):
        self.assertEqual(self.tokenDictionary.getToken(11, True), "wmv")

    def test_getSecondaryIndex(self):
        self.assertEqual(self.tokenDictionary.getIndex("wmv"), (11, True))