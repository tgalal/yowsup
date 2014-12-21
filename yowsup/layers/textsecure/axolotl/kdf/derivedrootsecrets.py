from ..util.byteutil import ByteUtil
class DerivedRootSecrets:
    SIZE = 64
    def __init__(self, okm):
        keys = ByteUtil.split(okm, 32, 32)
        self.rootKey = keys[0]
        self.chainKey = keys[1]

    def getRootKey(self):
        return self.rootKey

    def getChainKey(self):
        return self.chainKey
