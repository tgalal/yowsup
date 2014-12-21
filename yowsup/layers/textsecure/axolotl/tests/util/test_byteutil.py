import unittest
from yowsup.layers.textsecure.axolotl.util.byteutil import ByteUtil
class ByteUtilTest(unittest.TestCase):
    def test_split(self):
        okm = '02a9aa6c7dbd64f9d3aa92f92a277bf54609dadf0b00828acfc61e3c724b84a7bfbe5efb603030526742e3ee89c7024e884e' \
                 '440f1ff376bb2317b2d64deb7c8322f4c5015d9d895849411ba1d793a827'.decode('hex')

        data = [i for i in range(0, 80)]
        a_data = [i for i in range(0, 32)]
        b_data = [i for i in range(32, 64)]
        c_data = [i for i in range(64, 80)]

        a,b,c = ByteUtil.split(data, 32, 32, 16)

        self.assertEqual(a, a_data)
        self.assertEqual(b, b_data)
        self.assertEqual(c, c_data)
