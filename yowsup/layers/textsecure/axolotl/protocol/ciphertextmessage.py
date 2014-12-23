import abc
class CiphertextMessage(object):
    __metaclass__ = abc.ABCMeta

    UNSUPPORTED_VERSION = 1
    CURRENT_VERSION     = 3

    WHISPER_TYPE                = 2
    PREKEY_TYPE                 = 3
    SENDERKEY_TYPE              = 4
    SENDERKEY_DISTRIBUTION_TYPE = 5

    #This should be the worst case (worse than V2).  So not always accurate, but good enough for padding.
    ENCRYPTED_MESSAGE_OVERHEAD = 53
    @abc.abstractmethod
    def serialize(self):
        return

    @abc.abstractmethod
    def getType(self):
        return