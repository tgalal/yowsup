from yowsup.layers.textsecure.axolotl.state.sessionstore import SessionStore
from yowsup.layers.textsecure.axolotl.state.sessionrecord import SessionRecord
class InMemorySessionStore(SessionStore):
    def __init__(self):
        self.sessions = {}


    def loadSession(self, recepientId, deviceId):
        if self.containsSession(recepientId, deviceId):
            return SessionRecord(serialized=self.sessions[(recepientId, deviceId)])
        else:
            return SessionRecord()

    def getSubDeviceSessions(self, recepientId):
        deviceIds = []
        for k in self.sessions.keys():
            if k[0] == recepientId:
                deviceIds.append(k[1])

        return deviceIds

    def storeSession(self, recepientId, deviceId, sessionRecord):
        self.sessions[(recepientId, deviceId)] = sessionRecord.serialize()

    def containsSession(self, recepientId, deviceId):
        return (recepientId, deviceId) in self.sessions

    def deleteSession(self, recepientId, deviceId):
        del self.sessions[(recepientId, deviceId)]

    def deleteAllSessions(self, recepientId):
        for k in self.sessions.keys():
            if k[0] == recepientId:
                del self.sessions[k]



