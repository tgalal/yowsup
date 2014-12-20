class DjbECPublicKey:

    DJB_TYPE = b'\x05'

    def __init__(self, publicKey):
        self.publicKey = publicKey

    def serialize(self):
        return self.DJB_TYPE + self.publicKey

    def __eq__(self, other):
        return self.serialize() == other.serialize()

class DjbECPrivateKey:

    DJB_TYPE = b'\x05'

    def __init__(self, privateKey):
        self.privateKey = privateKey

    def serialize(self):
        return self.privateKey

    def __eq__(self, other):
        return self.serialize() == other.serialize()