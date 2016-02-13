# from yowsup.layers.protocol_media import mediacipher
import tempfile
import os
class DownloadableMediaMessageBuilder(object):
    def __init__(self, downloadbleMediaMessageClass, jid, filepath):
        self.jid = jid
        self.filepath = filepath
        self.encryptedFilepath = None
        self.cls = downloadbleMediaMessageClass
        self.mediaKey = None
        self.attributes = {}
        self.mediaType = self.cls.__name__.split("DownloadableMediaMessageProtocolEntity")[0].lower() #ugly ?

    # def encrypt(self):
    #     fd, encpath = tempfile.mkstemp()
    #     mediaKey = os.urandom(112)
    #     keys = mediacipher.getDerivedKeys(mediaKey)
    #     out = mediacipher.encryptImage(self.filepath, keys)
    #     with open(encImagePath, 'w') as outF:
    #         outF.write(out)
    #
    #     self.mediaKey = mediaKey
    #     self.encryptedFilepath = encpath

    # def decrypt(self):
    #     self.mediaKey = None
    #     self.encryptedFilePath = None


    def setEncryptionData(self, mediaKey, encryptedFilepath):
        self.mediaKey = mediaKey
        self.encryptedFilepath = encryptedFilepath

    def isEncrypted(self):
        return self.encryptedFilepath is not None

    def getFilepath(self):
        return self.encryptedFilepath or self.filepath

    def getOriginalFilepath(self):
        return self.filepath

    def set(self, key, val):
        self.attributes[key] = val

    def get(self, key, default = None):
        if key in self.attributes and self.attributes[key] is not None:
            return self.attributes[key]

        return default

    def getOrSet(self, key, func):
        if not self.get(key):
            self.set(key, func())

    def build(self, url = None, ip = None):
        if url:
            self.set("url", url)
        if ip:
            self.set("ip", ip)
        return self.cls.fromBuilder(self)
