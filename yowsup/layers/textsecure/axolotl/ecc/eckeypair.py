class ECKeyPair():

    def __init__(self, publicKey, privateKey):
        self.publicKey = publicKey
        self.privateKey = privateKey

    def getPrivateKey(self):
        return self.privateKey

    def getPublicKey(self):
        return self.publicKey

