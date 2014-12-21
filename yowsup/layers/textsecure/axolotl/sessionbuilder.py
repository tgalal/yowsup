import logging
from ratchet.bobaxolotlparamaters import BobAxolotlParameters
from ratchet.ratchetingsession import RatchetingSession
from .util.medium import Medium
logger = logging.getLogger(__name__)
class SessionBuilder:
    def __init__(self, sessionStore, preKeyStore, signedPreKeyStore, identityKeyStore, recepientId, deviceId):
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.signedPreKeyStore = signedPreKeyStore
        self.identityKeyStore = identityKeyStore
        self.recepientId = recepientId
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

        if not self.identityKeyStore.isTrustedIdentity(self.recepientId, theirIdentityKey):
            raise Exception("Untrusted identity!!")

        if messageVersion == 2:
            raise Exception("IMPL ME")
        elif messageVersion == 3:
            unsignedPreKeyId = self.processV3(sessionRecord, message)
        else:
            raise Exception("Unkown version %s" % messageVersion)

        self.identityKeyStore.saveIdentity(self.recepientId, theirIdentityKey)

        return unsignedPreKeyId

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
            .setOurIdentityKey(self.identityKeyStore.getIdentityKeyPair)\
            .setOurSignedPreKey(ourSignedPreKey)\
            .setOurRatchetKey(ourSignedPreKey)

        if message.getPreKeyId() is not None:
            parameters.setOurOneTimePreKey(self.preKeyStore.loadPreKey(message.getPreKeyId()).getKeyPair())
        else:
            parameters.setOurOneTimePreKey(None)

        if not sessionRecord.isFresh():
            sessionRecord.archiveCurrentState()

        RatchetingSession.initializeSession(sessionRecord.getSessionState(), message.getMessageVersion(), parameters.create())
        sessionRecord.getSessionState().setLocalRegistrationId(self.identityKeyStore.getLocalRegistrationId())
        sessionRecord.getSessionState().setRemoteRegistrationId(message.getRegistrationId())
        sessionRecord.getSessionState().setAliceBaseKey(message.getBaseKey().serialize())

        if message.getPreKeyId() is not None and message.getPreKeyId() != Medium.MAX_VALUE:
            return message.getPreKeyId()
        else:
            return None

