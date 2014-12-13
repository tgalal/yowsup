import unittest
from yowsup.layers.auth.keystream import KeyStream
class KeyStreamTest(unittest.TestCase):

    def setUp(self):

        self.password = bytearray(list(map(ord,"password")))
        self.salt     = bytearray(list(map(ord,"salt")))

        self.keysTarget = [
            bytearray(b'>\xd5\x8a\xecB\xdb\xc8\xd4}\x98\x9aBa\x89\x9fC\x08\xdcp\x8d'),
            bytearray(b'\xd3;\xda:\x8f\x94CX\xe4;\xbb\xcc"W\x83\xe0m\xba\xe0\xd1'),
            bytearray(b'\x92w{\xc2\x04~\x08;\x81w\xb7h3\xb8\xc4t\xbd\xed\xf7q'),
            bytearray(b'.\xc7\xe4\x15\x1a\xa0\xfd\x98\xc0\xea\xefs{\r7E\xa6\xec\xd5\xfb')
        ]

        self.pbkdbf2_res = bytearray(b'\xeal\x01M\xc7-o\x8c\xcd\x1e\xd9*\xce\x1dA\xf0\xd8\xde\x89W')
        self.inputMessage = bytearray([0,0,0,0, ord('t'), ord('a'), ord('r'), ord('e'), ord('k')])
        self.inputMessageComputedMac = bytearray(b'\xec\x82q\xab\x9f\x8d;\xac\x83\xc5X\xbb\xb6u\x1c\xb0\xd2\x82=`')
        self.inputMessageRC4Ciphered = bytearray(b'\x00\x00\x00\x00\xf4&-\x0c\xbc')


    def test_generateKeys(self):
        keys = KeyStream.generateKeys(self.password, self.salt)
        self.assertEqual(keys, self.keysTarget)

    def test_pbkdf2(self):
        result = KeyStream.pbkdf2(self.password, self.salt, 2, 20)
        result = bytearray(result)
        self.assertEqual(result, self.pbkdbf2_res)
    
    def test_computemac(self):
        keys = self.keysTarget
        kstream = KeyStream(keys[2], keys[3])
        res = kstream.computeMac(self.inputMessage, 4, len(self.inputMessage) - 4)
        self.assertEqual(res, self.inputMessageComputedMac)

    def test_rc4(self):
        keys = self.keysTarget
        kstream = KeyStream(keys[2], keys[3])
        kstream.rc4.cipher(self.inputMessage, 4, len(self.inputMessage) - 4)
        self.assertEqual(self.inputMessage, self.inputMessageRC4Ciphered)

    def test_encodeMessage(self):
        keys = self.keysTarget
        kstream = KeyStream(keys[2], keys[3])
        encoded = kstream.encodeMessage(self.inputMessage, 0, 4, len(self.inputMessage) - 4)

    def test_manyEncode(self):
        keys = self.keysTarget
        kstream = KeyStream(keys[2], keys[3])
        for i in xrange(0, 4294967299):
            encoded = kstream.encodeMessage(self.inputMessage, 0, 4, len(self.inputMessage) - 4)