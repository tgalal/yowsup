import abc
class IdentityKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def getIdentityKeyPair(self):pass

    @abc.abstractmethod
    def getLocalRegistrationId(self):pass

    @abc.abstractmethod
    def saveIdentity(self, recepientId, identityKey):pass

    @abc.abstractmethod
    def isTrustedIdentity(self, recepientId, identityKey):pass