from ..util.byteutil import ByteUtil
class DerivedMessageSecrets:
    SIZE              = 80
    CIPHER_KEY_LENGTH = 32
    MAC_KEY_LENGTH    = 32
    IV_LENGTH         = 16

    def __init__(self, okm):
        keys = ByteUtil.split(okm, self.__class__.CIPHER_KEY_LENGTH, self.__class__.MAC_KEY_LENGTH,
                              self.__class__.IV_LENGTH)
        self.cipherKey = keys[0] #AES
        self.macKey = keys[1] #sha256
        self.iv = keys[2]


    def getCipherKey(self):
        return self.cipherKey

    def getMacKey(self):
        return self.macKey

    def getIv(self):
        return self.iv
