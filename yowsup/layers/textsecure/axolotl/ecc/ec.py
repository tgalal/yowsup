import abc
class ECPublicKey(object):
    __metaclass__ = abc.ABCMeta
    KEY_SIZE = 33
    @abc.abstractmethod
    def serialize(self):pass

    @abc.abstractmethod
    def getType(self):pass

class ECPrivateKey(object):
    __metaclass__ = abc.ABCMeta
    @abc.abstractmethod
    def serialize(self):pass

    @abc.abstractmethod
    def getType(self):pass