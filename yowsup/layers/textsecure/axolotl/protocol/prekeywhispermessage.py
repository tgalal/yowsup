from .ciphertextmessage import CiphertextMessage
from ..util.byteutil import ByteUtil
from ..ecc.curve import Curve
from ..identitykey import IdentityKey
from .whispermessage import WhisperMessage
import whisperprotos
class PreKeyWhisperMessage(CiphertextMessage):
    def __init__(self, messageVersion = None, registrationId = None, preKeyId = None,
                 signedPreKeyId = None, ecPublicBaseKey = None, identityKey = None, whisperMessage = None, serialized = None):

        if serialized:
            self.version = ByteUtil.highBitsToInt(serialized[0])
            if self.version > CiphertextMessage.CURRENT_VERSION:
                raise Exception("Unknown version %s" % self.version)

            preKeyWhisperMessage = whisperprotos.PreKeyWhisperMessage()
            preKeyWhisperMessage.ParseFromString(serialized[1:])

            if (self.version == 2 and preKeyWhisperMessage.preKeyId is None) or\
                (self.version == 3 and preKeyWhisperMessage.signedPreKeyId is None) or\
                not preKeyWhisperMessage.baseKey or\
                not preKeyWhisperMessage.identityKey or \
                not preKeyWhisperMessage.message:

                raise Exception("Incomplete message")

            self.serialized = serialized
            self.registrationId = preKeyWhisperMessage.registrationId
            self.preKeyId       = preKeyWhisperMessage.preKeyId
            self.signedPreKeyId = preKeyWhisperMessage.signedPreKeyId if preKeyWhisperMessage.signedPreKeyId is not None else -1
            self.baseKey        = Curve.decodePoint(bytearray(preKeyWhisperMessage.baseKey), 0)

            self.identityKey    = IdentityKey(Curve.decodePoint(bytearray(preKeyWhisperMessage.identityKey), 0))
            self.message =  WhisperMessage(serialized = preKeyWhisperMessage.message)

        else:
            self.version = messageVersion
            self.registrationId = registrationId
            self.preKeyId = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey = ecPublicBaseKey
            self.identityKey = identityKey
            self.message = whisperMessage

            builder = whisperprotos.PreKeyWhisperMessage()
            builder.signedPreKeyId = signedPreKeyId
            builder.baseKey = ecPublicBaseKey.serialize()
            builder.identityKey = identityKey.serialize()
            builder.message = whisperMessage.serialize()
            builder.registrationId = registrationId

            if preKeyId is not None:
                builder.preKeyId = preKeyId

            versionBytes = ByteUtil.intsToByteHighAndLow(self.version, self.__class__.CURRENT_VERSION)
            messageBytes = builder.SerializeToString()
            self.serialized = str(ByteUtil.combine(versionBytes, messageBytes))

    def getMessageVersion(self):
        return self.version

    def getIdentityKey(self):
        return self.identityKey

    def getRegistrationId(self):
        return self.registrationId

    def getPreKeyId(self):
        return self.preKeyId

    def getSignedPreKeyId(self):
        return self.signedPreKeyId

    def getBaseKey(self):
        return self.baseKey

    def getWhisperMessage(self):
        return self.message

    def serialize(self):
        return self.serialized

    def getType(self):
        return CiphertextMessage.PREKEY_TYPE
