from yowsup.layers.coder.tokendictionary import TokenDictionary
import unittest
class TokenDictionaryTest(unittest.TestCase):
    def setUp(self):
        self.tokenDictionary = TokenDictionary()

    def test_getToken(self):
        self.assertEqual(self.tokenDictionary.getToken(74), "iq")

    def test_getIndex(self):
        self.assertEqual(self.tokenDictionary.getIndex("iq"), (74, False))

    def test_getSecondaryToken(self):
        self.assertEqual(self.tokenDictionary.getToken(238), "wmv")

    def test_getSecondaryTokenExplicit(self):
        self.assertEqual(self.tokenDictionary.getToken(1, True), "wmv")

    def test_getSecondaryIndex(self):
        self.assertEqual(self.tokenDictionary.getIndex("wmv"), (1, True))