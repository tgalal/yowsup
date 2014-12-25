import unittest
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.sessionbuilder import SessionBuilder
from axolotl.sessioncipher import SessionCipher
from yowsup.layers.textsecure.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from axolotl.tests.inmemoryaxolotlstore import InMemoryAxolotlStore
from axolotl.state.prekeybundle import PreKeyBundle
from axolotl.protocol.ciphertextmessage import CiphertextMessage

class DecryptTest(unittest.TestCase):
    BOB_RECIPIENT_ID = 4915731870097

    def setUp(self):
        pkmsgHex = "330891b3c903122105ff4d4194973db1a18ee52b1136a84e6901528ea612675948c11c141db27fe3321a21050be7f9848" \
                   "30b676fb615a62b207cb444632125eb8a39620b0eaf7ddfd5f442112242330a2105eb839d6891854068a3eaafff0e818" \
                   "bf5d529a372c7ec1e3a29eb40f2c388c17c1000180022101bf20894c38da270d241e328a412dced7059e67a3f72f994" \
                   "28bad6a0a3013000"

        self.pkgMsgSerialized = pkmsgHex.decode('hex')
        self.store = LiteAxolotlStore("/home/tarek/.yowsup/axolotarek.db")


    def test_pkmsgX(self):
        aliceStore = InMemoryAxolotlStore()
        aliceSessionBuilder = SessionBuilder(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)

        bobStore =   LiteAxolotlStore("/home/tarek/.yowsup/axolotarek.db")
        pk = bobStore.loadPreKeys()[5]
        bobPreKeyPair = pk.getKeyPair()
        sk =  bobStore.loadSignedPreKeys()[0]
        bobSignedPreKeyPair = sk.getKeyPair()
        bobSignedPreKeySignature = sk.getSignature()

        bobPreKey = PreKeyBundle(bobStore.getLocalRegistrationId(), 1,
                                              pk.getId(), bobPreKeyPair.getPublicKey(),
                                              sk.getId(), bobSignedPreKeyPair.getPublicKey(),
                                              bobSignedPreKeySignature,
                                              bobStore.getIdentityKeyPair().getPublicKey())

        aliceSessionBuilder.processPreKeyBundle(bobPreKey)
        self.assertTrue(aliceStore.containsSession(self.__class__.BOB_RECIPIENT_ID, 1))
        self.assertTrue(aliceStore.loadSession(self.__class__.BOB_RECIPIENT_ID, 1).getSessionState().getSessionVersion() == 3)

        originalMessage    = "HELLO BOB"
        aliceSessionCipher = SessionCipher(aliceStore, aliceStore, aliceStore, aliceStore, self.__class__.BOB_RECIPIENT_ID, 1)
        outgoingMessage    = aliceSessionCipher.encrypt(bytearray(originalMessage))

        self.assertTrue(outgoingMessage.getType() == CiphertextMessage.PREKEY_TYPE)

        incomingMessage = PreKeyWhisperMessage(serialized=outgoingMessage.serialize())

    def test_PkMsg(self):
        ALICE_ID = "4917675341470"
        BOB_ID = "4915731870097"
        msg = PreKeyWhisperMessage(serialized=self.pkgMsgSerialized)

        sessionBuilder = SessionBuilder(self.store, self.store, self.store, self.store, ALICE_ID, 1)
        sessionRecord = self.store.loadSession(ALICE_ID, 1)
        sessionBuilder.process(sessionRecord, msg)
        sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, ALICE_ID, 1)
        plaintext = sessionCipher.decryptPkmsg(msg)
        print(plaintext)
        #
        # result = sessionCipher.decryptPkmsg(msg)
        #
        # print result



