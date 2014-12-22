from yowsup.layers.textsecure.axolotl.state.prekeystore import PreKeyStore
from yowsup.layers.textsecure.axolotl.state.prekeyrecord import PreKeyRecord
class InMemoryPreKeyStore(PreKeyStore):
    def __init__(self):
        self.store = {}

    def loadPreKey(self, preKeyId):
        if preKeyId not in self.store:
            raise Exception("No such prekeyRecord!")

        return PreKeyRecord(serialized = self.store[preKeyId])

    def storePreKey(self, preKeyId, preKeyRecord):
        self.store[preKeyId] = preKeyRecord.serialize()

    def containsPreKey(self, preKeyId):
        return preKeyId in self.store

    def removePreKey(self, preKeyId):
        if preKeyId in self.store:
            del self.store[preKeyId]