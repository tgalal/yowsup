# coding=utf-8
import unittest
import time
from yowsup.layers.textsecure.axolotl.sessionbuilder import SessionBuilder
from yowsup.layers.textsecure.axolotl.sessioncipher import SessionCipher
from yowsup.layers.textsecure.axolotl.ecc.curve import Curve
from yowsup.layers.textsecure.axolotl.ecc.eckeypair import ECKeyPair
from yowsup.layers.textsecure.axolotl.protocol.ciphertextmessage import CiphertextMessage
from yowsup.layers.textsecure.axolotl.protocol.whispermessage import WhisperMessage
from yowsup.layers.textsecure.axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from yowsup.layers.textsecure.axolotl.state.prekeybundle import PreKeyBundle
from yowsup.layers.textsecure.axolotl.tests.inmemoryaxolotlstore import InMemoryAxolotlStore
from yowsup.layers.textsecure.axolotl.state.prekeyrecord import PreKeyRecord
from yowsup.layers.textsecure.axolotl.state.signedprekeyrecord import SignedPreKeyRecord
class SessionBuilderTest(unittest.TestCase):
    ALICE_RECIPIENT_ID = 5L
    BOB_RECIPIENT_ID   = 2L

    def test_basicPreKeyV2(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)


        bobStore      = InMemoryAxolotlStore()
        bobPreKeyPair = Curve.generateKeyPair()
        bobPreKey     = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                                  31337, bobPreKeyPair.getPublicKey(),
                                                  0, None, None,
                                                  bobStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID, 1).getSessionState().getSessionVersion() == 2)

        originalMessage    = "L'homme est condamné à être libre"
        aliceSessionCipher = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        outgoingMessage    = aliceSessionCipher.encrypt(bytearray(originalMessage))

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage(serialized=outgoingMessage.serialize())
        bobStore.storePreKey(31337, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))

        bobSessionCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)
        plaintext        = bobSessionCipher.decryptPkmsg(incomingMessage)

        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))
        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID, 1).getSessionState().getSessionVersion() == 2)
        self.assertEqual(originalMessage, plaintext)


        bobOutgoingMessage = bobSessionCipher.encrypt(bytearray(originalMessage))
        self.assertTrue(bobOutgoingMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        alicePlaintext = aliceSessionCipher.decryptMsg(bobOutgoingMessage)
        self.assertEqual(alicePlaintext, originalMessage)

        self.runInteraction(aliceStore, bobStore)

        aliceStore          = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        aliceSessionCipher  = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)

        bobPreKeyPair = Curve.generateKeyPair()
        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(),
                                 1, 31338, bobPreKeyPair.getPublicKey(),
                                 0, None, None, bobStore.getIdentityKeyPair().getPublicKey())

        bobStore.storePreKey(31338, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        outgoingMessage = aliceSessionCipher.encrypt(bytearray(originalMessage))
        try :
            bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            bobStore.saveIdentity(self.__class__.ALICE_RECIPIENT_ID, PreKeyWhisperMessage(serialized=outgoingMessage.serialize()).getIdentityKey())

        plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
        self.assertEqual(plaintext, originalMessage)

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                 31337, Curve.generateKeyPair().getPublicKey(),
                                 0, None, None,
                                 aliceStore.getIdentityKeyPair().getPublicKey())
        try:
            aliceSessionBuilder.processPreKeyBundle(bobPreKey)
            raise AssertionError("shouldn't be trusted")
        except Exception:
            #good
            pass

        return


    def test_basicPreKeyV3(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)

        bobStore =   InMemoryAxolotlStore()
        bobPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeyPair = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(bobStore.getIdentityKeyPair().getPrivateKey(),
                                                                           bobSignedPreKeyPair.getPublicKey().serialize())

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                              31337, bobPreKeyPair.getPublicKey(),
                                              22, bobSignedPreKeyPair.getPublicKey(),
                                              bobSignedPreKeySignature,
                                              bobStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)
        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID, 1).getSessionState().getSessionVersion() == 3)

        originalMessage    = "L'homme est condamné à être libre"
        aliceSessionCipher = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        outgoingMessage    = aliceSessionCipher.encrypt(bytearray(originalMessage))

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage(serialized=outgoingMessage.serialize())
        bobStore.storePreKey(31337, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        bobStore.storeSignedPreKey(22, SignedPreKeyRecord(22, int(time.time() * 1000), bobSignedPreKeyPair, bobSignedPreKeySignature))

        bobSessionCipher = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)

        plaintext = bobSessionCipher.decryptPkmsg(incomingMessage)
        self.assertEqual(originalMessage, plaintext)
        # @@TODO: in callback assertion
        # self.assertFalse(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(bobStore.containsSession(self.__class__.ALICE_RECIPIENT_ID, 1))

        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID, 1).getSessionState().getSessionVersion() == 3)
        self.assertTrue(bobStore.loadSession(self.__class__.ALICE_RECIPIENT_ID, 1).getSessionState().getAliceBaseKey() != None)
        self.assertEqual(originalMessage, plaintext)

        bobOutgoingMessage = bobSessionCipher.encrypt(bytearray(originalMessage))
        self.assertTrue(bobOutgoingMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        alicePlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobOutgoingMessage.serialize()))
        self.assertEqual(alicePlaintext, originalMessage)

        self.runInteraction(aliceStore, bobStore)

        aliceStore          = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        aliceSessionCipher  = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)

        bobPreKeyPair            = Curve.generateKeyPair()
        bobSignedPreKeyPair      = Curve.generateKeyPair()
        bobSignedPreKeySignature = Curve.calculateSignature(bobStore.getIdentityKeyPair().getPrivateKey(), bobSignedPreKeyPair.getPublicKey().serialize())
        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(),
                                 1, 31338, bobPreKeyPair.getPublicKey(),
                                 23, bobSignedPreKeyPair.getPublicKey(), bobSignedPreKeySignature,
                                 bobStore.getIdentityKeyPair().getPublicKey())

        bobStore.storePreKey(31338, PreKeyRecord(bobPreKey.getPreKeyId(), bobPreKeyPair))
        bobStore.storeSignedPreKey(23, SignedPreKeyRecord(23, int(time.time() * 1000), bobSignedPreKeyPair, bobSignedPreKeySignature))
        aliceSessionBuilder.processPreKeyBundle(bobPreKey)

        outgoingMessage = aliceSessionCipher.encrypt(bytearray(originalMessage))

        try:
            plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage))
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            bobStore.saveIdentity(self.__class__.ALICE_RECIPIENT_ID, PreKeyWhisperMessage(serialized=outgoingMessage.serialize()).getIdentityKey())

        plaintext = bobSessionCipher.decryptPkmsg(PreKeyWhisperMessage(serialized=outgoingMessage.serialize()))
        self.assertEqual(plaintext, originalMessage)


        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                 31337, Curve.generateKeyPair().getPublicKey(),
                                 23, bobSignedPreKeyPair.getPublicKey(), bobSignedPreKeySignature,
                                 aliceStore.getIdentityKeyPair().getPublicKey())
        try:
            aliceSessionBuilder.process(bobPreKey)
            raise AssertionError("shouldn't be trusted!")
        except Exception:
            #good
            pass

    def runInteraction(self, aliceStore, bobStore):
        """
        :type aliceStore: AxolotlStore
        :type  bobStore: AxolotlStore
        """

        aliceSessionCipher = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        bobSessionCipher   = SessionCipher(bobStore, bobStore, bobStore, bobStore, self.__class__.ALICE_RECIPIENT_ID, 1)

        originalMessage = "smert ze smert"
        aliceMessage = aliceSessionCipher.encrypt(bytearray(originalMessage))

        self.assertTrue(aliceMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceMessage.serialize()))
        self.assertEqual(plaintext, originalMessage)

        bobMessage = bobSessionCipher.encrypt(bytearray(originalMessage))

        self.assertTrue(bobMessage.getType() == CiphertextMessage.WHISPER_TYPE)

        plaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobMessage.serialize()))
        self.assertEqual(plaintext, originalMessage)

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                             "We mean that man first of all exists, encounters himself, " \
                             "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(bytearray(loopingMessage))
            loopingPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceLoopingMessage.serialize()))
            self.assertEqual(loopingPlaintext, loopingMessage)


        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            bobLoopingMessage = bobSessionCipher.encrypt(bytearray(loopingMessage))

            loopingPlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobLoopingMessage.serialize()))
            self.assertEqual(loopingPlaintext, loopingMessage)

        aliceOutOfOrderMessages = []

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(bytearray(loopingMessage))
            aliceOutOfOrderMessages.append((loopingMessage, aliceLoopingMessage))

        for i in range(0, 10):
            loopingMessage = "What do we mean by saying that existence precedes essence? " \
                 "We mean that man first of all exists, encounters himself, " \
                 "surges up in the world--and defines himself aftward. %s" % i
            aliceLoopingMessage = aliceSessionCipher.encrypt(bytearray(loopingMessage))
            loopingPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceLoopingMessage.serialize()))
            self.assertEqual(loopingPlaintext, loopingMessage)

        for i in range(0, 10):
            loopingMessage = "You can only desire based on what you know: %s" % i
            bobLoopingMessage = bobSessionCipher.encrypt(bytearray(loopingMessage))

            loopingPlaintext = aliceSessionCipher.decryptMsg(WhisperMessage(serialized=bobLoopingMessage.serialize()))
            self.assertEqual(loopingPlaintext, loopingMessage)

        for aliceOutOfOrderMessage in aliceOutOfOrderMessages:
            outOfOrderPlaintext = bobSessionCipher.decryptMsg(WhisperMessage(serialized=aliceOutOfOrderMessage[1].serialize()))
            self.assertEqual(outOfOrderPlaintext, aliceOutOfOrderMessage[0])
