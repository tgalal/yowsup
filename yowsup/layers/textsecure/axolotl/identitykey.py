from ecc.curve import Curve
class IdentityKey:
    def __init__(self, ecPubKeyOrBytes, offset = None):
        if offset is None:
            self.publicKey = ecPubKeyOrBytes
        else:
            self.publicKey = Curve.decodePoint(bytearray(ecPubKeyOrBytes), offset)

    def getPublicKey(self):
        return self.publicKey

    def serialize(self):
        return self.publicKey.serialize()

    def get_fingerprint(self):
        raise Exception("IMPL ME")

    def __eq__(self, other):
        return self.publicKey == other.getPublicKey()

    def hashCode(self):
        raise Exception("IMPL ME")

