from ..ecc.curve import Curve
from ..kdf.derivedrootsecrets import DerivedRootSecrets
from chainkey import ChainKey
class RootKey:
    def __init__(self, kdf, key):
        self.kdf = kdf
        self.key = key

    def getKeyBytes(self):
        return self.key

    def createChain(self, ECPublicKey_theirRatchetKey, ECKeyPair_ouRatchetKey):
        sharedSecret = Curve.calculateAgreement(ECPublicKey_theirRatchetKey, ECKeyPair_ouRatchetKey.getPrivateKey())
        derivedSecretBytes = self.kdf.deriveSecrets(sharedSecret, self.key, "WhisperRatchet".getBytes(), DerivedRootSecrets.SIZE)
        derivedSecrets = DerivedRootSecrets(derivedSecretBytes)
        newRootKey = RootKey(derivedSecrets.getRootKey())
        newChainKey = ChainKey(self.kdf, derivedSecrets.getChainKey(), 0)
        return (newRootKey, newChainKey)
