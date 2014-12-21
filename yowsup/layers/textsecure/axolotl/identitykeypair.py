from state.storageprotos import IdentityKeyPairStructure
from identitykey import IdentityKey
from ecc.curve import Curve
class IdentityKeyPair:
    def __init__(self, identityKeyPublicKey = None, ecPrivateKey = None, serialized = None):
        if serialized:
            structure = IdentityKeyPairStructure()
            structure.ParseFromString(serialized)
            self.publicKey = IdentityKey(bytearray(structure.publicKey), offset = 0)
            self.privateKey = Curve.decodePrivatePoint(bytearray(structure.privateKey))
        else:
            self.publicKey = identityKeyPublicKey
            self.privateKey = ecPrivateKey

    def getPublicKey(self):
        return self.publicKey

    def getPrivateKey(self):
        return self.privateKey

    def serialize(self):
        structure = IdentityKeyPairStructure()
        structure.publicKey = self.publicKey.serialize()
        structure.privateKey = self.privateKey.serialize()
        return structure.SerializeToString()