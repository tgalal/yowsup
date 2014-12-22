from yowsup.layers.textsecure.axolotl.state.axolotlstore import AxolotlStore
from yowsup.layers.textsecure.axolotl.tests.inmemoryidentitykeystore import InMemoryIdentityKeyStore
from yowsup.layers.textsecure.axolotl.tests.inmemoryprekeystore import InMemoryPreKeyStore
from yowsup.layers.textsecure.axolotl.tests.inmemorysessionstore import InMemorySessionStore
from yowsup.layers.textsecure.axolotl.tests.inmemorysignedprekeystore import InMemorySignedPreKeyStore
class InMemoryAxolotlStore(AxolotlStore):
    def __init__(self):
        self.identityKeyStore = InMemoryIdentityKeyStore()
        self.preKeyStore = InMemoryPreKeyStore()
        self.signedPreKeyStore = InMemorySignedPreKeyStore()
        self.sessionStore = InMemorySessionStore()

    def getIdentityKeyPair(self):
        return self.identityKeyStore.getIdentityKeyPair()

    def getLocalRegistrationId(self):
        return self.identityKeyStore.getLocalRegistrationId()

    def saveIdentity(self, recepientId, identityKey):
        self.identityKeyStore.saveIdentity(recepientId, identityKey)

    def isTrustedIdentity(self, recepientId, identityKey):
        return self.identityKeyStore.isTrustedIdentity(recepientId, identityKey)

    def loadPreKey(self, preKeyId):
        return self.preKeyStore.loadPreKey(preKeyId)

    def storePreKey(self, preKeyId, preKeyRecord):
        self.preKeyStore.storePreKey(preKeyId, preKeyRecord)

    def containsPreKey(self, preKeyId):
        return self.preKeyStore.containsPreKey(preKeyId)

    def removePreKey(self, preKeyId):
        self.preKeyStore.removePreKey(preKeyId)

    def loadSession(self, recepientId, deviceId):
        return self.sessionStore.loadSession(recepientId, deviceId)

    def getSubDeviceSessions(self, recepientId):
        return self.sessionStore.getSubDeviceSessions(recepientId)

    def storeSession(self, recepientId, deviceId, sessionRecord):
        self.sessionStore.storeSession(recepientId, deviceId, sessionRecord)

    def containsSession(self, recepientId, deviceId):
        return self.sessionStore.containsSession(recepientId, deviceId)

    def deleteSession(self, recepientId, deviceId):
        self.sessionStore.deleteSession(recepientId, deviceId)

    def deleteAllSessions(self, recepientId):
        self.sessionStore.deleteAllSessions(recepientId)

    def loadSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.loadSignedPreKey(signedPreKeyId)

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.signedPreKeyStore.storeSignedPreKey(signedPreKeyId, signedPreKeyRecord)

    def containsSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey(signedPreKeyId)

    def removeSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey(signedPreKeyId)
