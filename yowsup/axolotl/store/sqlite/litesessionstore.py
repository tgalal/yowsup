from axolotl.state.sessionstore import SessionStore
from axolotl.state.sessionrecord import SessionRecord
import sys
class LiteSessionStore(SessionStore):
    def __init__(self, dbConn):
        """
        :type dbConn: Connection
        """
        self.dbConn = dbConn
        dbConn.execute("CREATE TABLE IF NOT EXISTS sessions (_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "recipient_id INTEGER UNIQUE, device_id INTEGER, record BLOB, timestamp INTEGER);")


    def loadSession(self, recipientId, deviceId):
        q = "SELECT record FROM sessions WHERE recipient_id = ? AND device_id = ?"
        c = self.dbConn.cursor()
        c.execute(q, (recipientId, deviceId))
        result = c.fetchone()

        if result:
            return SessionRecord(serialized=result[0])
        else:
            return SessionRecord()

    def getSubDeviceSessions(self, recipientId):
        q = "SELECT device_id from sessions WHERE recipient_id = ?"
        c = self.dbConn.cursor()
        c.execute(q, (recipientId,))
        result = c.fetchall()

        deviceIds = [r[0] for r in result]
        return deviceIds

    def storeSession(self, recipientId, deviceId, sessionRecord):
        self.deleteSession(recipientId, deviceId)

        q = "INSERT INTO sessions(recipient_id, device_id, record) VALUES(?,?,?)"
        c = self.dbConn.cursor()
        serialized = sessionRecord.serialize()
        c.execute(q, (recipientId, deviceId, buffer(serialized) if sys.version_info < (2,7) else serialized))
        self.dbConn.commit()

    def containsSession(self, recipientId, deviceId):
        q = "SELECT record FROM sessions WHERE recipient_id = ? AND device_id = ?"
        c = self.dbConn.cursor()
        c.execute(q, (recipientId, deviceId))
        result = c.fetchone()

        return result is not None

    def deleteSession(self, recipientId, deviceId):
        q = "DELETE FROM sessions WHERE recipient_id = ? AND device_id = ?"
        self.dbConn.cursor().execute(q, (recipientId, deviceId))
        self.dbConn.commit()

    def deleteAllSessions(self, recipientId):
        q = "DELETE FROM sessions WHERE recipient_id = ?"
        self.dbConn.cursor().execute(q, (recipientId,))
        self.dbConn.commit()
