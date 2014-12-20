from storageprotos import SignedPreKeyRecordStructure
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
class SignedPreKeyRecord:
    def __init__(self, _id = None, timestamp = None, ecKeyPair = None, signature = None, serialized = None):
        self.structure = SignedPreKeyRecordStructure()
        if serialized:
            self.structure.ParseFromString(serialized)
        else:
            self.structure.id = _id
            self.structure.publicKey = ecKeyPair.getPublicKey().serialize()
            self.structure.privateKey = ecKeyPair.getPrivateKey().serialize()
            self.structure.signature = signature
            self.structure.timestamp = timestamp


    def getId(self):
        return self.structure.id

    def getTimestamp(self):
        return self.structure.timestamp

    def getKeyPair(self):
        publicKey = Curve.decodePoint(bytearray(self.structure.publicKey), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self.structure.privateKey))

        return ECKeyPair(publicKey, privateKey)

    def getSignature(self):
        return self.structure.signature

    def serialize(self):
        return self.structure.SerializeToString()