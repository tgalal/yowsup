from yowsup.layers import YowLayer
from protocolentities import SetKeysIqProtocolEntity
from axolotl.util.keyhelper import KeyHelper
from store.sqlite.liteaxolotlstore import LiteAxolotlStore
from axolotl.sessionbuilder import SessionBuilder
from axolotl.state.signedprekeyrecord import SignedPreKeyRecord
import binascii


class YowTextSecureLayer(YowLayer):
    EVENT_PREKEYS_SET = "org.openwhatsapp.yowsup.events.textsecure.set"
    TYPE_DJB = 0x5
    def __init__(self):
        super(YowTextSecureLayer, self).__init__()
        self.store = store = LiteAxolotlStore("/home/tarek/.yowsup/axolotarek.db")
        self.session = SessionBuilder(store, store, store, store, 10, 20)

    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        self.toUpper(data)

    def onEvent(self, yowLayerEvent):
        if yowLayerEvent.getName() == self.__class__.EVENT_PREKEYS_SET:
            self.sendKeys()
    def adjustArray(self, arr):
        return binascii.hexlify(arr).decode('hex')

    def adjustId(self, _id):
        _id = format(_id, 'x').zfill(6)
        # if len(_id) % 2:
        #     _id = "0" + _id
        return binascii.unhexlify(_id)


    def sendKeys(self):
        self.genKeys()
        return
        identityKeyPair = self.store.getIdentityKeyPair()
        registrationId = self.store.getLocalRegistrationId()
        preKeys = self.store.loadPreKeys()[:2]
        signedPreKey = self.store.loadSignedPreKeys()[0]

        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))


        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))


        print(setKeysIq.toProtocolTreeNode())

        # self.toLower(setKeysIq.toProtocolTreeNode())


    def genKeys(self):
        identityKeyPair     = KeyHelper.generateIdentityKeyPair()
        registrationId      = KeyHelper.generateRegistrationId()
        preKeys             = KeyHelper.generatePreKeys(7493876, 200)
        signedPreKey        = KeyHelper.generateSignedPreKey(identityKeyPair, 0)


        self.store.storeLocalData(registrationId, identityKeyPair)
        self.store.storeSignedPreKey(signedPreKey.getId(), signedPreKey)

        preKeysDict = {}
        for preKey in preKeys:
            self.store.storePreKey(preKey.getId(), preKey)
            keyPair = preKey.getKeyPair()
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))


        print registrationId
        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))
        self.toLower(setKeysIq.toProtocolTreeNode())

