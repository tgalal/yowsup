import abc
class SessionStore(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def loadSession(self, recepientId, deviceId):pass

    @abc.abstractmethod
    def getSubDeviceSessions(self, recepientId): pass

    @abc.abstractmethod
    def storeSession(self, recepientId, deviceId, sessionRecord):pass

    @abc.abstractmethod
    def containsSession(self, recepientId, deviceId): pass

    @abc.abstractmethod
    def deleteSession(self, recepientId, deviceId): pass

    @abc.abstractmethod
    def deleteAllSessions(self, recepientId): pass