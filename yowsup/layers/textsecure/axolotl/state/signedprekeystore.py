import abc
class SignedPreKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadSignedPreKey(self, signedPreKeyId):pass

    @abc.abstractmethod
    def loadSignedPreKeys(self):pass

    @abc.abstractmethod
    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord): pass

    @abc.abstractmethod
    def containsSignedPreKey(self, signedPreKeyId): pass

    @abc.abstractmethod
    def removeSignedPreKey(self, signedPreKeyId): pass