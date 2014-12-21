import abc
class PreKeyStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadPreKey(self, preKeyId):pass

    @abc.abstractmethod
    def storePreKey(self, preKeyId, preKeyRecord):pass

    @abc.abstractmethod
    def containsPreKey(self, preKeyId):pass

    @abc.abstractmethod
    def removePreKey(self, preKeyId):pass