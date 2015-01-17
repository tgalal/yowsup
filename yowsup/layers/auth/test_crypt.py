from yowsup.layers import YowLayerEvent, YowLayerTest
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.auth import YowCryptLayer
from yowsup.layers.auth.keystream import KeyStream

class CryptLayerTest(YowLayerTest, YowCryptLayer):
    def setUp(self):
        YowCryptLayer.__init__(self)
        self.password = bytearray(list(map(ord,"password")))
        self.salt     = bytearray(list(map(ord,"salt")))
        self.username = "username"
        self.inputMessage = bytearray([0,0,0,0, ord('t'), ord('a'), ord('r'), ord('e'), ord('k')])
        self.inputMessageCrypted = bytearray(b'\x80\x00\r)\x99\xbe_\xee\x98\xecV<\x9d\x0c\xb7r')
        keys = [
            bytearray(b'>\xd5\x8a\xecB\xdb\xc8\xd4}\x98\x9aBa\x89\x9fC\x08\xdcp\x8d'),
            bytearray(b'\xd3;\xda:\x8f\x94CX\xe4;\xbb\xcc"W\x83\xe0m\xba\xe0\xd1'),
            bytearray(b'\x92w{\xc2\x04~\x08;\x81w\xb7h3\xb8\xc4t\xbd\xed\xf7q'),
            bytearray(b'.\xc7\xe4\x15\x1a\xa0\xfd\x98\xc0\xea\xefs{\r7E\xa6\xec\xd5\xfb')
        ]
        inputKey = KeyStream(keys[2], keys[3])
        outputKey = KeyStream(keys[0], keys[1])

        self.onEvent(YowLayerEvent(YowCryptLayer.EVENT_KEYS_READY, keys = (inputKey, outputKey)))

    def test_00send(self):
        self.send(self.inputMessage)
        self.assertEqual(self.lowerSink.pop(), self.inputMessageCrypted)

