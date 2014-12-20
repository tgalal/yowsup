class ECKeyPair():
    KEY_SIZE = 33
    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

    def getPrivateKey(self):
        return self.privateKey

    def getPublicKey(self):
        return self.publicKey

    def __eq__(self, other):
        return self.publicKey == other.getPublicKey() and self.privateKey == other.getPrivateKey()