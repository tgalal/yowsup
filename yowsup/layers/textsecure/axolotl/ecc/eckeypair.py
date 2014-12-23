class ECKeyPair():

    def __init__(self, publicKey, privateKey):
        """
        :type publicKey: ECPublicKey
        :type privateKey: ECPrivateKey
        """
        self.publicKey = publicKey
        self.privateKey = privateKey

    def getPrivateKey(self):
        return self.privateKey

    def getPublicKey(self):
        return self.publicKey

