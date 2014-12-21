from ciphertextmessage import CipherTextMessage
from ..util.byteutil import ByteUtil
from ..ecc.curve import Curve
import whisperprotos
import hmac
import hashlib
class WhisperMessage(CipherTextMessage):
    MAC_LENGTH = 8

    def __init__(self, messageVersion = None, macKey = None, ECPublicKey_senderRatchetKey = None,
                 counter = None, previousCounter = None, ciphertext = None,
                 senderIdentityKey = None, receiverIdentityKey = None,
                 serialized = None):

        if serialized:
            messageParts = ByteUtil.split(serialized, 1, len(serialized) - 1 - WhisperMessage.MAC_LENGTH,
                                          WhisperMessage.MAC_LENGTH)
            version = messageParts[0][0]
            message = messageParts[1]
            mac = messageParts[2]

            if ByteUtil.highBitsToInt(version) <= self.__class__.UNSUPPORTED_VERSION:
                raise Exception("Legacy message %s" % ByteUtil.highBitsToInt(version))

            if ByteUtil.highBitsToInt(version) > self.__class__.CURRENT_VERSION:
                raise Exception("Unknown version: %s" % ByteUtil.highBitsToInt(version))

            whisperMessage = whisperprotos.WhisperMessage()
            whisperMessage.ParseFromString(message)

            if not whisperMessage.ciphertext or whisperMessage.counter is None or not whisperMessage.ratchetKey:
                raise Exception("Incomplete message")

            self.serialized = serialized
            self.senderRatchetKey = Curve.decodePoint(bytearray(whisperMessage.ratchetKey), 0)
            self.messageVersion = ByteUtil.highBitsToInt(version)
            self.counter = whisperMessage.counter
            self.previousCounter = whisperMessage.previousCounter
            self.ciphertext = whisperMessage.ciphertext
        else:
            version  = ByteUtil.intsToByteHighAndLow(messageVersion, self.__class__.CURRENT_VERSION)
            message = whisperprotos.WhisperMessage()
            message.ratchetKey = ECPublicKey_senderRatchetKey.serialize()
            message.counter = counter
            message.previousCounter = previousCounter
            message.ciphertext = ciphertext
            message = message.SerializeToString()

            mac  = self.getMac(messageVersion, senderIdentityKey, receiverIdentityKey, macKey,
                               ByteUtil.combine(version, message))
            self.serialized = ByteUtil.combine(version, message, mac)
            self.senderRatchetKey = ECPublicKey_senderRatchetKey
            self.counter = counter
            self.previousCounter = previousCounter
            self.ciphertext = ciphertext
            self.messageVersion = messageVersion


    def getSenderRatchetKey(self):
        return self.senderRatchetKey

    def getMessageVersion(self):
        return self.messageVersion

    def getCounter(self):
        return self.counter

    def getBody(self):
        return self.ciphertext

    def verifyMac(self, messageVersion, senderIdentityKey, receiverIdentityKey, macKey):
        parts = ByteUtil.split(self.serialized, len(self.serialized) - self.__class__.MAC_LENGTH, self.__class__.MAC_LENGTH)
        ourMac = self.getMac(messageVersion, senderIdentityKey, receiverIdentityKey, macKey, parts[0])
        theirMac = parts[1]

        if ourMac != theirMac:
            raise Exception("Bad Mac!")

    def getMac(self, messageVersion, senderIdentityKey, receiverIdentityKey, macKey, serialized):
        mac = hmac.new(macKey, digestmod=hashlib.sha256)
        if messageVersion >= 3:
            mac.update(senderIdentityKey.getPublicKey().serialize())
            mac.update(receiverIdentityKey.getPublickKey().serialize())

        fullMac = mac.update(serialized)
        return ByteUtil.trim(fullMac, self.__class__.MAC_LENGTH)

    def serialize(self):
        return self.serialized

    def getType(self):
        return CipherTextMessage.WHISPER_TYPE

    def isLegacy(self, message):
        return message is not None and len(message) >= 1 and ByteUtil.highBitsToInt(message[0]) <= CipherTextMessage.UNSUPPORTED_VERSION

    # def getMac(self, macKey, serialized):
    #     fullMac = hmac.new(macKey, serialized, digestmod=hashlib.sha256).digest()
    #     return fullMac[:self.MAC_LENGTH]

    # def verifyMac(self, macKey):
    #     ourMac = self.getMac( macKey, self.serialized[:len(self.serialized) - self.MAC_LENGTH] )
    #     theirMac = self.serialized[len(self.serialized) - self.MAC_LENGTH:][:self.MAC_LENGTH]
    #
    #     if not ourMac == theirMac:
    #         print( "Bad Mac! (inside WhisperMessage verifyMac)")





