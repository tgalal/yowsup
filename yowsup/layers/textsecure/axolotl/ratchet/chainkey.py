import hmac
import hashlib
from ..kdf.derivedmessagesecrets import DerivedMessageSecrets
from ..kdf.messagekeys import MessageKeys
class ChainKey:
    MESSAGE_KEY_SEED    = bytearray([0x01])
    CHAIN_KEY_SEED      = bytearray([0x02])

    def __init__(self, kdf, key, index):
        self.kdf = kdf
        self.key = key
        self.index = index

    def getKey(self):
        return self.key

    def getIndex(self):
        return self.index

    def getNextChainKey(self):
        nextKey = self.getBaseMaterial(self.__class__.CHAIN_KEY_SEED)
        return ChainKey(self.kdf, nextKey, self.index + 1)

    def getMessageKeys(self):
        inputKeyMaterial = self.getBaseMaterial(self.__class__.MESSAGE_KEY_SEED)
        keyMaterialBytes = self.kdf.deriveSecrets(inputKeyMaterial, bytearray("WhisperMessageKeys"), DerivedMessageSecrets.SIZE)
        keyMaterial = DerivedMessageSecrets(keyMaterialBytes)
        return MessageKeys(keyMaterial.getCipherKey(), keyMaterial.getMacKey(), keyMaterial.getIv(), self.index)

    def getBaseMaterial(self, seedBytes):
        mac = hmac.new(self.key, digestmod=hashlib.sha256)
        mac.update(seedBytes)
        return mac.digest()

