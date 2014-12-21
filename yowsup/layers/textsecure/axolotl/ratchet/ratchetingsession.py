from ..ecc.curve import Curve
from .bobaxolotlparamaters import BobAxolotlParameters
from ..kdf.hkdf import HKDF
from ..util.byteutil import ByteUtil
from .rootkey import RootKey
from .chainkey import ChainKey

class RatchetingSession:
    @staticmethod
    def initializeSession(sessionState, sessionVersion, parameters):
        """
        :type sessionState: SessionState
        :type sessionVersion: int
        :type parameters: SymmetricAxolotlParameters
        """

        if RatchetingSession.isAlice(parameters.getOurBaseKey().getPublicKey(), parameters.getTheirBaseKey()):
            raise Exception("IMPL ALICE SESSION!")
        else:
            bobParameters = BobAxolotlParameters.newBuilder()
            bobParameters.setOurIdentityKey(parameters.getOurIdentityKey())\
                   .setOurRatchetKey(parameters.getOurRatchetKey())\
                   .setOurSignedPreKey(parameters.getOurBaseKey())\
                   .setOurOneTimePreKey(None)\
                   .setTheirBaseKey(parameters.getTheirBaseKey())\
                   .setTheirIdentityKey(parameters.getTheirIdentityKey())
            RatchetingSession.initializeSessionAsBob(sessionState, sessionVersion, bobParameters.create())

    @staticmethod
    def initializeSessionAsBob(sessionState, sessionVersion, parameters):
        """
        :type sessionState: SessionState
        :type sessionVersion: int
        :type parameters: BobAxolotlParameters
        """

        sessionState.setSessionVersion(sessionVersion)
        sessionState.setRemoteIdentityKey(parameters.getTheirIdentityKey())
        sessionState.setLocalIdentityKey(parameters.getOurIdentityKey().getPublicKey())

        secrets = bytearray()

        if sessionState >= 3:
            secrets.extend(RatchetingSession.getDiscontinuityBytes())

        secrets.extend(Curve.calculateAgreement(parameters.getTheirIdentityKey().getPublicKey(),
                                                parameters.getOurSignedPreKey().getPrivateKey()))

        secrets.extend(Curve.calculateAgreement(parameters.getTheirBaseKey(),
                                                parameters.getOurIdentityKey().getPrivateKey()))
        secrets.extend(Curve.calculateAgreement(parameters.getTheirBaseKey(),
                                               parameters.getOurSignedPreKey().getPrivateKey()))

        if sessionVersion >= 3 and parameters.getOurOneTimePreKey() is not None:
            secrets.write(Curve.calculateAgreement(parameters.getTheirBaseKey(),
                                                   parameters.getOurOneTimePreKey().getPrivateKey()))

        derivedKeys = RatchetingSession.calculateDerivedKeys(sessionVersion, secrets)
        sessionState.setSenderChain(parameters.getOurRatchetKey(), derivedKeys.getChainKey())
        sessionState.setRootKey(derivedKeys.getRootKey())


    @staticmethod
    def getDiscontinuityBytes():
        return bytearray([0xFF] * 32)

    @staticmethod
    def calculateDerivedKeys(sessionVersion, masterSecret):
        kdf = HKDF.createFor(sessionVersion)
        derivedSecretBytes = kdf.deriveSecrets(masterSecret,  "WhisperText".getBytes(), 64)
        derivedSecrets = ByteUtil.split(derivedSecretBytes, 32, 32)
        return RatchetingSession.DerivedKeys(RootKey(kdf, derivedSecrets[0]),
                                             ChainKey(kdf, derivedSecrets[1], 0))

    @staticmethod
    def isAlice(ourKey, theirKey, ecPublicKey):
        """
        :type ourKey: ECPublicKey
        :type theirKey: ECPublicKey
        """
        return ourKey < theirKey


    class DerivedKeys:
        def __init__(self, rootKey, chainKey):
            self.rootKey = rootKey
            self.chainKey = chainKey

        def getRootKey(self):
            return self.rootKey

        def getChainKey(self):
            return self.chainKey
