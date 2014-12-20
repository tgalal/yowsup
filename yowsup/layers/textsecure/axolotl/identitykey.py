from ecc.curve import Curve
class IdentityKey:
    def __init__(self, ecPubKey = None, _bytes = None, offset = None):
        if ecPubKey:
            self.publicKey = ecPubKey
        else:
            self.publicKey = Curve.decodePoint(_bytes, offset)

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

