import unittest
from yowsup.layers.textsecure.axolotl.state.prekeyrecord import PreKeyRecord
from yowsup.layers.textsecure.axolotl.util.keyhelper import KeyHelper
from yowsup.layers.textsecure.axolotl.identitykeypair import IdentityKeyPair
from yowsup.layers.textsecure.axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
import binascii

class PreKeyRecordTest(unittest.TestCase):
    # def setUp(self):
    #     # prekeyData = [8, 244, 177, 201, 3, 18, 33, 5, 149, 51, 115, 242, 14, 157, 85, 6, 109, 210, 177, 98, 220, 19, 213,
    #     #         75, 241, 123, 167, 194, 237, 150, 109, 58, 106, 215, 84, 20, 6, 214, 46, 9, 26, 32, 208, 159, 248,
    #     #         113, 188, 164, 65, 168, 80, 157, 67, 39, 197, 78, 210, 171, 156, 2, 58, 43, 22, 85, 234, 68, 2, 23,
    #     #         33, 90, 77, 44, 211, 84]
    #     # prekeyData = bytearray(prekeyData)
    #     preKey = "346800831fc052d2a81e28785bc398d9ce0afb4ba54a8adad8933decc88b5339"
    #     preKey = preKey.decode('hex')
    #
    #     rec = PreKeyRecord(serialized=preKey)

    def test_pk(self):
        preKey = "08f4b1c903122105953373f20e9d55066dd2b162dc13d54bf17ba7c2ed966d3a6ad7541406d62e091a20d09ff871bca441a8" \
                 "509d4327c54ed2ab9c023a2b1655ea440217215a4d2cd354"
        preKey = preKey.decode('hex')

        rec = PreKeyRecord(serialized=preKey)
        keyPair = rec.getKeyPair()


    def test_pkmsg(self):
        pkmsg = "330892b2c903122105be5a1a08c87f3c95c4a6b32923818980c797dcb39875080ca55dceddb11771291a21050be7f98483" \
                "0b676fb615a62b207cb444632125eb8a39620b0eaf7ddfd5f442112242330a21055736a868cbe1989457ac8fa77258129" \
                "cdde09564879c9e1eb2c500300b0a3228100018002210ce92e9f44b80e0b59c130e7dc87db44c2f2c293d3d56e65028ba" \
                "d6a0a3013000".decode('hex')


        m = PreKeyWhisperMessage(serialized=pkmsg)

        print(m)


    def test_identity(self):
        identityKeyPair = KeyHelper.generateIdentityKeyPair()
        serialized = identityKeyPair.serialize()
        en = binascii.hexlify(serialized)
        serialized = binascii.unhexlify(en)

        #signed = KeyHelper.generateSignedPreKey(identityKeyPair, 0)
        #kpair = signed.getKeyPair()
        #pub = kpair.getPublicKey().serialize()
        #l = len(signed.getSignature())
        #pubh = binascii.hexlify(pub)


        identityKeyPair2 = IdentityKeyPair(serialized = serialized)

        x = identityKeyPair2.getPrivateKey().serialize()
        x = binascii.hexlify(x)

        self.assertEqual(identityKeyPair.getPublicKey(), identityKeyPair2.getPublicKey())
        self.assertEqual(identityKeyPair.getPrivateKey(), identityKeyPair2.getPrivateKey())





