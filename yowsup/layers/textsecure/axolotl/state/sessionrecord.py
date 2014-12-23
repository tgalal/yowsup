import storageprotos
from sessionstate import SessionState
class SessionRecord:
    ARCHIVED_STATES_MAX_LENGTH = 40
    def __init__(self, sessionState = None, serialized = None):
        """
        :type sessionState: SessionState
        :type serialized: str
        """
        self.previousStates = []
        if sessionState:
            self.sessionState = sessionState
            self.fresh = False
        elif serialized:
            record = storageprotos.RecordStructure()
            record.ParseFromString(serialized)
            self.sessionState = SessionState(record.currentSession)
            self.fresh = False
            for previousStructure in record.previousSessions:
                self.previousStates.append(SessionState(previousStructure))

        else:
            self.fresh = True
            self.sessionState = SessionState()

    def hasSessionState(self, version, aliceBaseKey):
        if self.sessionState.getSessionVersion() == version and aliceBaseKey == self.sessionState.getAliceBaseKey():
            return True

        for state in self.previousStates:
            if state.getSessionVersion() == version and aliceBaseKey == state.getAliceBaseKey():
                return True

        return False


    def getSessionState(self):
        return self.sessionState

    def getPreviousSessionStates(self):
        return self.previousStates

    def isFresh(self):
        return self.fresh

    def archiveCurrentState(self):
        self.promoteState(SessionState())

    def promoteState(self, promotedState):
        self.previousStates.insert(0, self.sessionState)
        self.sessionState = promotedState
        if len(self.previousStates) > self.__class__.ARCHIVED_STATES_MAX_LENGTH:
            self.previousStates.pop()


    def setState(self, sessionState):
        self.sessionState = sessionState

    def serialize(self):
        previousStructures = [previousState.getStructure() for previousState in self.previousStates]
        record = storageprotos.RecordStructure()
        record.currentSession.MergeFrom(self.sessionState.getStructure())
        record.previousSessions.extend(previousStructures)

        return record.SerializeToString()

