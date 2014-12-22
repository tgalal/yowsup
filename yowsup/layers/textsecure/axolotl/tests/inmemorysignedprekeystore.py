from yowsup.layers.textsecure.axolotl.state.signedprekeystore import SignedPreKeyStore
from yowsup.layers.textsecure.axolotl.state.signedprekeyrecord import SignedPreKeyRecord
class InMemorySignedPreKeyStore(SignedPreKeyStore):
    def __init__(self):
        self.store = {}

    def loadSignedPreKey(self, signedPreKeyId):
        if not signedPreKeyId in self.store:
            raise Exception("No such signedprekeyrecord! %s " % signedPreKeyId)

        return SignedPreKeyRecord(self.store[signedPreKeyId])

    def loadSignedPreKeys(self):
        results = []
        for serialized in self.store.values():
            results.append(SignedPreKeyRecord(serialized=serialized))

        return results

    def storeSignedPreKey(self, signedPreKeyId, signedPreKeyRecord):
        self.store[signedPreKeyId] = signedPreKeyRecord.serialize()

    def containsSignedPreKey(self, signedPreKeyId):
        return signedPreKeyId in self.store

    def removeSignedPreKey(self, signedPreKeyId):
        del self.store[signedPreKeyId]