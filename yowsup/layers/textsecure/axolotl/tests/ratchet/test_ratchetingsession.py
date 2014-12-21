import unittest
from yowsup.layers.textsecure.axolotl.identitykey import IdentityKey
from yowsup.layers.textsecure.axolotl.identitykeypair import IdentityKeyPair
from yowsup.layers.textsecure.axolotl.ecc.curve import Curve
from yowsup.layers.textsecure.axolotl.ecc.eckeypair import ECKeyPair
from yowsup.layers.textsecure.axolotl.ratchet.bobaxolotlparamaters import BobAxolotlParameters
from yowsup.layers.textsecure.axolotl.state.sessionstate import SessionState
from yowsup.layers.textsecure.axolotl.ratchet.ratchetingsession import RatchetingSession
class RatchetingSessionTest(unittest.TestCase):
    def test_ratchetingSessionAsBob(self):
        bobPublic   = bytearray([0x05, 0x2c, 0xb4, 0x97,
                                    0x76, 0xb8, 0x77, 0x02,
                                    0x05, 0x74, 0x5a, 0x3a,
                                    0x6e, 0x24, 0xf5, 0x79,
                                    0xcd, 0xb4, 0xba, 0x7a,
                                    0x89, 0x04, 0x10, 0x05,
                                    0x92, 0x8e, 0xbb, 0xad,
                                    0xc9, 0xc0, 0x5a, 0xd4,
                                    0x58])

        bobPrivate  = bytearray([0xa1, 0xca, 0xb4, 0x8f,
                                    0x7c, 0x89, 0x3f, 0xaf,
                                    0xa9, 0x88, 0x0a, 0x28,
                                    0xc3, 0xb4, 0x99, 0x9d,
                                    0x28, 0xd6, 0x32, 0x95,
                                    0x62, 0xd2, 0x7a, 0x4e,
                                    0xa4, 0xe2, 0x2e, 0x9f,
                                    0xf1, 0xbd, 0xd6, 0x5a])

        bobIdentityPublic   = bytearray([0x05, 0xf1, 0xf4, 0x38,
                                    0x74, 0xf6, 0x96, 0x69,
                                    0x56, 0xc2, 0xdd, 0x47,
                                    0x3f, 0x8f, 0xa1, 0x5a,
                                    0xde, 0xb7, 0x1d, 0x1c,
                                    0xb9, 0x91, 0xb2, 0x34,
                                    0x16, 0x92, 0x32, 0x4c,
                                    0xef, 0xb1, 0xc5, 0xe6,
                                    0x26])

        bobIdentityPrivate    = bytearray([0x48, 0x75, 0xcc, 0x69,
                                    0xdd, 0xf8, 0xea, 0x07,
                                    0x19, 0xec, 0x94, 0x7d,
                                    0x61, 0x08, 0x11, 0x35,
                                    0x86, 0x8d, 0x5f, 0xd8,
                                    0x01, 0xf0, 0x2c, 0x02,
                                    0x25, 0xe5, 0x16, 0xdf,
                                    0x21, 0x56, 0x60, 0x5e])

        aliceBasePublic     = bytearray([0x05, 0x47, 0x2d, 0x1f,
                                    0xb1, 0xa9, 0x86, 0x2c,
                                    0x3a, 0xf6, 0xbe, 0xac,
                                    0xa8, 0x92, 0x02, 0x77,
                                    0xe2, 0xb2, 0x6f, 0x4a,
                                    0x79, 0x21, 0x3e, 0xc7,
                                    0xc9, 0x06, 0xae, 0xb3,
                                    0x5e, 0x03, 0xcf, 0x89,
                                    0x50])

        aliceEphemeralPublic  = bytearray([0x05, 0x6c, 0x3e, 0x0d,
                                    0x1f, 0x52, 0x02, 0x83,
                                    0xef, 0xcc, 0x55, 0xfc,
                                    0xa5, 0xe6, 0x70, 0x75,
                                    0xb9, 0x04, 0x00, 0x7f,
                                    0x18, 0x81, 0xd1, 0x51,
                                    0xaf, 0x76, 0xdf, 0x18,
                                    0xc5, 0x1d, 0x29, 0xd3,
                                    0x4b])

        aliceIdentityPublic   = bytearray([0x05, 0xb4, 0xa8, 0x45,
                                    0x56, 0x60, 0xad, 0xa6,
                                    0x5b, 0x40, 0x10, 0x07,
                                    0xf6, 0x15, 0xe6, 0x54,
                                    0x04, 0x17, 0x46, 0x43,
                                    0x2e, 0x33, 0x39, 0xc6,
                                    0x87, 0x51, 0x49, 0xbc,
                                    0xee, 0xfc, 0xb4, 0x2b,
                                    0x4a])

        senderChain           = bytearray([0xd2, 0x2f, 0xd5, 0x6d, 0x3f,
                                    0xec, 0x81, 0x9c, 0xf4, 0xc3,
                                    0xd5, 0x0c, 0x56, 0xed, 0xfb,
                                    0x1c, 0x28, 0x0a, 0x1b, 0x31,
                                    0x96, 0x45, 0x37, 0xf1, 0xd1,
                                    0x61, 0xe1, 0xc9, 0x31, 0x48,
                                    0xe3, 0x6b])

        bobIdentityKeyPublic   = IdentityKey(bobIdentityPublic, 0)
        bobIdentityKeyPrivate  = Curve.decodePrivatePoint(bobIdentityPrivate)
        bobIdentityKey         =  IdentityKeyPair(bobIdentityKeyPublic, bobIdentityKeyPrivate)
        bobEphemeralPublicKey  = Curve.decodePoint(bobPublic, 0)
        bobEphemeralPrivateKey = Curve.decodePrivatePoint(bobPrivate)
        bobEphemeralKey        = ECKeyPair(bobEphemeralPublicKey, bobEphemeralPrivateKey)
        bobBaseKey             = bobEphemeralKey

        aliceBasePublicKey       = Curve.decodePoint(aliceBasePublic, 0)
        aliceEphemeralPublicKey  = Curve.decodePoint(aliceEphemeralPublic, 0)
        aliceIdentityPublicKey   = IdentityKey(aliceIdentityPublic, 0)

        parameters = BobAxolotlParameters.newBuilder()\
        .setOurIdentityKey(bobIdentityKey)\
        .setOurSignedPreKey(bobBaseKey)\
        .setOurRatchetKey(bobEphemeralKey)\
        .setOurOneTimePreKey(None)\
        .setTheirIdentityKey(aliceIdentityPublicKey)\
        .setTheirBaseKey(aliceBasePublicKey)\
        .create()

        session = SessionState()

        RatchetingSession.initializeSessionAsBob(session, 2, parameters)
        self.assertEqual(session.getLocalIdentityKey(), bobIdentityKey.getPublicKey())
        self.assertEqual(session.getRemoteIdentityKey(), aliceIdentityPublicKey)
        self.assertEqual(session.getSenderChainKey().getKey(), senderChain)
