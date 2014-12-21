from ..ecc.curve import Curve
from ..kdf.derivedrootsecrets import DerivedRootSecrets
from chainkey import ChainKey
class RootKey:
    def __init__(self, kdf, key):
        self.kdf = kdf
        self.key = key

    def getKeyBytes(self):
        return self.key

    def createChain(self, ECPublicKey_theirRatchetKey, ECKeyPair_ourRatchetKey):
        sharedSecret = Curve.calculateAgreement(ECPublicKey_theirRatchetKey, ECKeyPair_ourRatchetKey.getPrivateKey())
        derivedSecretBytes = self.kdf.deriveSecrets(sharedSecret, bytearray("WhisperRatchet"), DerivedRootSecrets.SIZE, salt = self.key)
        derivedSecrets = DerivedRootSecrets(derivedSecretBytes)
        newRootKey = RootKey(self.kdf, derivedSecrets.getRootKey())
        newChainKey = ChainKey(self.kdf, derivedSecrets.getChainKey(), 0)
        return (newRootKey, newChainKey)
