from axolotl.state.prekeystore import PreKeyStore
from axolotl.state.prekeyrecord import PreKeyRecord
import sys
class LitePreKeyStore(PreKeyStore):
    def __init__(self, dbConn):
        """
        :type dbConn: Connection
        """
        self.dbConn = dbConn
        dbConn.execute("CREATE TABLE IF NOT EXISTS prekeys (_id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "prekey_id INTEGER UNIQUE, sent_to_server BOOLEAN, record BLOB);")

    def loadPreKey(self, preKeyId):
        q = "SELECT record FROM prekeys WHERE prekey_id = ?"

        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))

        result = cursor.fetchone()
        if not result:
            raise Exception("No such prekeyRecord!")

        return PreKeyRecord(serialized = result[0])

    def loadPendingPreKeys(self):
        q = "SELECT record FROM prekeys"
        cursor = self.dbConn.cursor()
        cursor.execute(q)
        result = cursor.fetchall()

        return [PreKeyRecord(serialized=result[0]) for result in result]

    def storePreKey(self, preKeyId, preKeyRecord):
        #self.removePreKey(preKeyId)
        q = "INSERT INTO prekeys (prekey_id, record) VALUES(?,?)"
        cursor = self.dbConn.cursor()
        serialized = preKeyRecord.serialize()
        cursor.execute(q, (preKeyId, buffer(serialized) if sys.version_info < (2,7) else serialized))
        self.dbConn.commit()

    def containsPreKey(self, preKeyId):
        q = "SELECT record FROM prekeys WHERE prekey_id = ?"
        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))
        return cursor.fetchone() is not None

    def removePreKey(self, preKeyId):
        q = "DELETE FROM prekeys WHERE prekey_id = ?"
        cursor = self.dbConn.cursor()
        cursor.execute(q, (preKeyId,))
        self.dbConn.commit()
