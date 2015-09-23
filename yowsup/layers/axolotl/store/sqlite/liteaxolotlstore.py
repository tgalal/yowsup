from axolotl.state.axolotlstore import AxolotlStore
from .liteidentitykeystore import LiteIdentityKeyStore
from .liteprekeystore import LitePreKeyStore
from .litesessionstore import LiteSessionStore
from .litesignedprekeystore import LiteSignedPreKeyStore
import sqlite3
class LiteAxolotlStore(AxolotlStore):
    def __init__(self, db):
        conn = sqlite3.connect(db, check_same_thread=False)
        conn.text_factory = bytes
        self.identityKeyStore = LiteIdentityKeyStore(conn)
        self.preKeyStore =  LitePreKeyStore(conn)
        self.signedPreKeyStore = LiteSignedPreKeyStore(conn)
        self.sessionStore = LiteSessionStore(conn)

    def getIdentityKeyPair(self):
        return self.identityKeyStore.getIdentityKeyPair()

    def storeLocalData(self, registrationId, identityKeyPair):
        self.identityKeyStore.storeLocalData(registrationId, identityKeyPair)

    def getLocalRegistrationId(self):
        return self.identityKeyStore.getLocalRegistrationId()

    def saveIdentity(self, recepientId, identityKey):
        self.identityKeyStore.saveIdentity(recepientId, identityKey)

    def isTrustedIdentity(self, recepientId, identityKey):
        return self.identityKeyStore.isTrustedIdentity(recepientId, identityKey)

    def loadPreKey(self, preKeyId):
        return self.preKeyStore.loadPreKey(preKeyId)

    def loadPreKeys(self):
        return self.preKeyStore.loadPendingPreKeys()

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

    def loadSignedPreKeys(self):
        return self.signedPreKeyStore.loadSignedPreKeys()

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.signedPreKeyStore.storeSignedPreKey(signedPreKeyId, signedPreKeyRecord)

    def containsSignedPreKey(self, signedPreKeyId):
        return self.signedPreKeyStore.containsSignedPreKey(signedPreKeyId)

    def removeSignedPreKey(self, signedPreKeyId):
        self.signedPreKeyStore.removeSignedPreKey(signedPreKeyId)