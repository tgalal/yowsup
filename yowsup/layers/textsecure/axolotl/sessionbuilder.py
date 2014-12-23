import logging
from ratchet.bobaxolotlparamaters import BobAxolotlParameters
from ratchet.ratchetingsession import RatchetingSession
from .ecc.curve import Curve
from .util.medium import Medium
from .ratchet.aliceaxolotlparameters import AliceAxolotlParameters
from .ratchet.bobaxolotlparamaters import BobAxolotlParameters
logger = logging.getLogger(__name__)
class SessionBuilder:
    def __init__(self, sessionStore, preKeyStore, signedPreKeyStore, identityKeyStore, recepientId, deviceId):
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.signedPreKeyStore = signedPreKeyStore
        self.identityKeyStore = identityKeyStore
        self.recipientId = recepientId
        self.deviceId = deviceId

    def process(self, sessionRecord, message):
        """
        :param sessionRecord:
        :param message:
        :type message: PreKeyWhisperMessage
        """

        messageVersion = message.getMessageVersion()
        theirIdentityKey = message.getIdentityKey()

        unsignedPreKeyId = None

        if not self.identityKeyStore.isTrustedIdentity(self.recipientId, theirIdentityKey):
            raise Exception("Untrusted identity!!")

        if messageVersion == 2:
            unsignedPreKeyId = self.processV2(sessionRecord, message)
        elif messageVersion == 3:
            unsignedPreKeyId = self.processV3(sessionRecord, message)
        else:
            raise Exception("Unkown version %s" % messageVersion)

        self.identityKeyStore.saveIdentity(self.recipientId, theirIdentityKey)

        return unsignedPreKeyId


    def processV2(self, sessionRecord, message):
        """
        :type sessionRecord: SessionRecord
        :type message: PreKeyWhisperMessage
        """

        if message.getPreKeyId() is None:
            raise Exception("V2 message requires one time prekey id!")

        if not self.preKeyStore.containsPreKey(message.getPreKeyId()) and\
            self.sessionStore.containsSession(self.recipientId, self.deviceId):
            logging.warn("We've already processed the prekey part of this V2 session, letting bundled message fall through...")
            return None

        ourPreKey = self.preKeyStore.loadPreKey(message.getPreKeyId()).getKeyPair()

        parameters = BobAxolotlParameters.newBuilder()

        parameters.setOurIdentityKey(self.identityKeyStore.getIdentityKeyPair())\
              .setOurSignedPreKey(ourPreKey)\
              .setOurRatchetKey(ourPreKey)\
              .setOurOneTimePreKey(None)\
              .setTheirIdentityKey(message.getIdentityKey())\
              .setTheirBaseKey(message.getBaseKey())

        if not sessionRecord.isFresh():  sessionRecord.archiveCurrentState()

        RatchetingSession.initializeSessionAsBob(sessionRecord.getSessionState(), message.getMessageVersion(), parameters.create())

        sessionRecord.getSessionState().setLocalRegistrationId(self.identityKeyStore.getLocalRegistrationId())
        sessionRecord.getSessionState().setRemoteRegistrationId(message.getRegistrationId())
        sessionRecord.getSessionState().setAliceBaseKey(message.getBaseKey().serialize())

        if message.getPreKeyId() != Medium.MAX_VALUE:
            return message.getPreKeyId()
        else:
            return None


    def processV3(self, sessionRecord, message):
        """

        :param sessionRecord:
        :param message:
        :type message: PreKeyWhisperMessage
        :return:
        """

        if sessionRecord.hasSessionState(message.getMessageVersion(), message.getBaseKey().serialize()):
            logger.warn("We've already setup a session for this V3 message, letting bundled message fall through...")
            return None

        ourSignedPreKey = self.signedPreKeyStore.loadSignedPreKey(message.getSignedPreKeyId()).getKeyPair()
        parameters = BobAxolotlParameters.newBuilder()
        parameters.setTheirBaseKey(message.getBaseKey())\
            .setTheirIdentityKey(message.getIdentityKey())\
            .setOurIdentityKey(self.identityKeyStore.getIdentityKeyPair())\
            .setOurSignedPreKey(ourSignedPreKey)\
            .setOurRatchetKey(ourSignedPreKey)

        if message.getPreKeyId() is not None:
            parameters.setOurOneTimePreKey(self.preKeyStore.loadPreKey(message.getPreKeyId()).getKeyPair())
        else:
            parameters.setOurOneTimePreKey(None)

        if not sessionRecord.isFresh():
            sessionRecord.archiveCurrentState()

        RatchetingSession.initializeSessionAsBob(sessionRecord.getSessionState(), message.getMessageVersion(), parameters.create())
        sessionRecord.getSessionState().setLocalRegistrationId(self.identityKeyStore.getLocalRegistrationId())
        sessionRecord.getSessionState().setRemoteRegistrationId(message.getRegistrationId())
        sessionRecord.getSessionState().setAliceBaseKey(message.getBaseKey().serialize())

        if message.getPreKeyId() is not None and message.getPreKeyId() != Medium.MAX_VALUE:
            return message.getPreKeyId()
        else:
            return None


    def processPreKeyBundle(self, preKey):
        """
        :type preKey: PreKeyBundle
        """
        if not self.identityKeyStore.isTrustedIdentity(self.recipientId, preKey.getIdentityKey()):
            raise Exception("Untrusted ID !!")

        if preKey.getSignedPreKey() is not None and\
            not Curve.verifySignature(preKey.getIdentityKey().getPublicKey(),
                                      preKey.getSignedPreKey().serialize(),
                                      preKey.getSignedPreKeySignature()) :
            raise Exception("Invalid signature on device key!")

        if preKey.getSignedPreKey() is None and preKey.getPreKey() is None:
            raise Exception("Both signed and unsigned prekeys are absent!")

        supportsV3 = preKey.getSignedPreKey() is not None
        sessionRecord        = self.sessionStore.loadSession(self.recipientId, self.deviceId)
        ourBaseKey           = Curve.generateKeyPair()
        theirSignedPreKey    = preKey.getSignedPreKey() if supportsV3 else preKey.getPreKey()
        theirOneTimePreKey   = preKey.getPreKey()
        theirOneTimePreKeyId = preKey.getPreKeyId() if theirOneTimePreKey is not None else None

        parameters = AliceAxolotlParameters.newBuilder()

        parameters.setOurBaseKey(ourBaseKey)\
                .setOurIdentityKey(self.identityKeyStore.getIdentityKeyPair())\
                .setTheirIdentityKey(preKey.getIdentityKey())\
                .setTheirSignedPreKey(theirSignedPreKey)\
                .setTheirRatchetKey(theirSignedPreKey)\
                .setTheirOneTimePreKey(theirOneTimePreKey if supportsV3 else None)

        if not sessionRecord.isFresh(): sessionRecord.archiveCurrentState();

        RatchetingSession.initializeSessionAsAlice(sessionRecord.getSessionState(),
                                                   3 if supportsV3 else 2,
                                                   parameters.create())

        sessionRecord.getSessionState().setUnacknowledgedPreKeyMessage(theirOneTimePreKeyId, preKey.getSignedPreKeyId(), ourBaseKey.getPublicKey())
        sessionRecord.getSessionState().setLocalRegistrationId(self.identityKeyStore.getLocalRegistrationId())
        sessionRecord.getSessionState().setRemoteRegistrationId(preKey.getRegistrationId())
        sessionRecord.getSessionState().setAliceBaseKey(ourBaseKey.getPublicKey().serialize())
        self.sessionStore.storeSession(self.recipientId, self.deviceId, sessionRecord)
        self.identityKeyStore.saveIdentity(self.recipientId, preKey.getIdentityKey())

