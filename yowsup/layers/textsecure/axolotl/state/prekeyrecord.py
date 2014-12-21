from storageprotos import PreKeyRecordStructure
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
class PreKeyRecord:
    def __init__(self, _id = None, ecKeyPair = None, serialized = None):
        self.structure = PreKeyRecordStructure()
        if serialized:
            self.structure.ParseFromString(serialized)
        else:
            self.structure.id = _id
            self.structure.publicKey = ecKeyPair.getPublicKey().serialize()
            self.structure.privateKey = ecKeyPair.getPrivateKey().serialize()

    def getId(self):
        return self.structure.id

    def getKeyPair(self):
        publicKey = Curve.decodePoint(bytearray(self.structure.publicKey), 0)
        privateKey = Curve.decodePrivatePoint(bytearray(self.structure.privateKey))
        return ECKeyPair(publicKey, privateKey)

    def serialize(self):
        return self.structure.SerializeToString()
