class MessageKeys:
    def __init__(self, cipherKey, macKey, iv, counter):
        self.cipherKey = cipherKey
        self.macKey = macKey
        self.iv = iv
        self.counter = counter

    def getCipherKey(self):
        return self.cipherKey

    def getMacKey(self):
        return self.macKey

    def getIv(self):
        return self.iv

    def getCounter(self):
        return self.counter