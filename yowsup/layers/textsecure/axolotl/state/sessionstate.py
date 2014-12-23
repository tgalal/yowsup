import storageprotos
from ..identitykeypair import IdentityKey,IdentityKeyPair
from ..ratchet.rootkey import RootKey
from ..kdf.hkdf import HKDF
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from ..ratchet.chainkey import ChainKey
from ..kdf.messagekeys import MessageKeys
class SessionState:
    def __init__(self, session = None):

        if session == None:
            self.sessionStructure = storageprotos.SessionStructure()
        elif session.__class__ == SessionState:
            self.sessionStructure = storageprotos.SessionStructure()
            self.sessionStructure.CopyFrom(session.sessionStructure)
        else:
            self.sessionStructure = session

    def getStructure(self):
        return self.sessionStructure

    def getAliceBaseKey(self):
        return self.sessionStructure.aliceBaseKey

    def setAliceBaseKey(self, aliceBaseKey):
        self.sessionStructure.aliceBaseKey = aliceBaseKey


    def setSessionVersion(self, version):
        self.sessionStructure.sessionVersion = version

    def getSessionVersion(self):
        sessionVersion = self.sessionStructure.sessionVersion
        return 2 if sessionVersion == 0 else sessionVersion

    def setRemoteIdentityKey(self, identityKey):
        self.sessionStructure.remoteIdentityPublic = identityKey.serialize()

    def setLocalIdentityKey(self, identityKey):
        self.sessionStructure.localIdentityPublic = identityKey.serialize()


    def getRemoteIdentityKey(self):
        if self.sessionStructure.remoteIdentityPublic is None:
            return None
        return IdentityKey(self.sessionStructure.remoteIdentityPublic, 0)

    def getLocalIdentityKey(self):
        return IdentityKey(self.sessionStructure.localIdentityPublic, 0)

    def getPreviousCounter(self):
        return self.sessionStructure.previousCounter

    def setPreviousCounter(self, previousCounter):
        self.sessionStructure.previousCounter = previousCounter


    def getRootKey(self):
        return RootKey(HKDF.createFor(self.getSessionVersion()), self.sessionStructure.rootKey)

    def setRootKey(self, rootKey):
        self.sessionStructure.rootKey = rootKey.getKeyBytes()


    def getSenderRatchetKey(self):
        return Curve.decodePoint(bytearray(self.sessionStructure.senderChain.senderRatchetKey), 0)

    def getSenderRatchetKeyPair(self):
        publicKey = self.getSenderRatchetKey()
        privateKey = Curve.decodePrivatePoint(self.sessionStructure.senderChain.senderRatchetKeyPrivate)

        return ECKeyPair(publicKey, privateKey)

    def hasReceiverChain(self, ECPublickKey_senderEphemeral):
        return self.getReceiverChain(ECPublickKey_senderEphemeral) is not None

    def hasSenderChain(self):
        return self.sessionStructure.HasField("senderChain")

    def getReceiverChain(self, ECPublickKey_senderEphemeral):
        receiverChains = self.sessionStructure.receiverChains
        index = 0
        for receiverChain in receiverChains:
            chainSenderRatchetKey = Curve.decodePoint(bytearray(receiverChain.senderRatchetKey), 0)
            if chainSenderRatchetKey == ECPublickKey_senderEphemeral:
                return (receiverChain, index)

            index += 1

    def getReceiverChainKey(self, ECPublicKey_senderEphemeral):
        receiverChainAndIndex = self.getReceiverChain(ECPublicKey_senderEphemeral)
        receiverChain = receiverChainAndIndex[0]
        if receiverChain is None:
            return None

        return ChainKey(HKDF.createFor(self.getSessionVersion()),
                        receiverChain.chainKey.key,
                        receiverChain.chainKey.index)

    def addReceiverChain(self, ECPublickKey_senderRatchetKey, chainKey):
        senderRatchetKey = ECPublickKey_senderRatchetKey


        chain = storageprotos.SessionStructure.Chain()
        chain.senderRatchetKey = senderRatchetKey.serialize()
        chain.chainKey.key = chainKey.getKey()
        chain.chainKey.index = chainKey.getIndex()

        self.sessionStructure.receiverChains.extend([chain])

        if len(self.sessionStructure.receiverChains) > 5:
            self.sessionStructure.receiverChains.remove(0)


    def setSenderChain(self, ECKeyPair_senderRatchetKeyPair, chainKey):
        senderRatchetKeyPair = ECKeyPair_senderRatchetKeyPair

        senderChain = storageprotos.SessionStructure.Chain()

        self.sessionStructure.senderChain.senderRatchetKey = senderRatchetKeyPair.getPublicKey().serialize()
        self.sessionStructure.senderChain.senderRatchetKeyPrivate = senderRatchetKeyPair.getPrivateKey().serialize()
        self.sessionStructure.senderChain.chainKey.key = chainKey.key
        self.sessionStructure.senderChain.chainKey.index = chainKey.index


    def getSenderChainKey(self):
        chainKeyStructure = self.sessionStructure.senderChain.chainKey
        return ChainKey(HKDF.createFor(self.getSessionVersion()),
                        chainKeyStructure.key, chainKeyStructure.index)

    def setSenderChainKey(self, ChainKey_nextChainKey):
        nextChainKey = ChainKey_nextChainKey

        self.sessionStructure.senderChain.chainKey.key = nextChainKey.getKey()
        self.sessionStructure.senderChain.chainKey.index = nextChainKey.getIndex()


    def hasMessageKeys(self, ECPublickKey_senderEphemeral, counter):
        senderEphemeral =ECPublickKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        if chain is None:
            return False

        messageKeyList = chain.messageKeys
        for messageKey in messageKeyList:
            if messageKey.index == counter:
                return True

        return False

    def removeMessageKeys(self, ECPublicKey_senderEphemeral, counter):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        if chain is None:
            return None

        messageKeyList = chain.messageKeys
        result = None

        for i in range(0, len(messageKeyList)):
            messageKey = messageKeyList[i]
            if messageKey.index == counter:
                result = MessageKeys(messageKey.cipherKey, messageKey.macKey, messageKey.iv, messageKey.index)
                del messageKeyList[i]
                break

        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)

        return result

    def setMessageKeys(self, ECPublicKey_senderEphemeral, messageKeys):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        messageKeyStructure = chain.messageKeys.add() #storageprotos.SessionStructure.Chain.MessageKey()
        messageKeyStructure.cipherKey = messageKeys.getCipherKey()
        messageKeyStructure.macKey = messageKeys.getMacKey()
        messageKeyStructure.index = messageKeys.getCounter()
        messageKeyStructure.iv = messageKeys.getIv()


        #chain.messageKeys.append(messageKeyStructure)

        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)


    def setReceiverChainKey(self, ECPublicKey_senderEphemeral, chainKey):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        chain.chainKey.key = chainKey.getKey()
        chain.chainKey.index = chainKey.getIndex()

        #self.sessionStructure.receiverChains[chainAndIndex[1]].ClearField()
        self.sessionStructure.receiverChains[chainAndIndex[1]].CopyFrom(chain)


    def setPendingKeyExchange(self, sequence, ourBaseKey, ourRatchetKey, ourIdentityKey):
        """
        :type sequence: int
        :type ourBaseKey: ECKeyPair
        :type ourRatchetKey: ECKeyPair
        :type  ourIdentityKey: IdentityKeyPair
        """

        structure = self.sessionStructure.PendingKeyExchange()
        structure.sequence = sequence
        structure.localBaseKey = ourBaseKey.getPublicKey().serialize()
        structure.localBaseKeyPrivate = ourBaseKey.getPrivateKey().serialize()
        structure.localRatchetKey = ourRatchetKey.getPublicKey().serialize()
        structure.localRatchetKeyPrivate = ourRatchetKey.getPrivateKey().serialize()
        structure.localIdentityKey = ourIdentityKey.getPublicKey().serialize()
        structure.localIdentityKeyPrivate = ourIdentityKey.getPrivateKey().serialize()

        self.sessionStructure.pendingKeyExchange.MergeFrom(structure)


    def getPendingKeyExchangeSequence(self):
        return self.sessionStructure.pendingKeyExchange.sequence

    def getPendingKeyExchangeBaseKey(self):
        publicKey = Curve.decodePoint(bytearray(self.sessionStructure.pendingKeyExchange.localBaseKey), 0)
        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pendingKeyExchange.localBaseKeyPrivate)
        return ECKeyPair(publicKey, privateKey)


    def getPendingKeyExchangeRatchetKey(self):
        publicKey = Curve.decodePoint(bytearray(self.sessionStructure.pendingKeyExchange.localRatchetKey), 0)
        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pendingKeyExchange.localRatchetKeyPrivate)
        return ECKeyPair(publicKey, privateKey)


    def getPendingKeyExchangeIdentityKey(self):
        publicKey = IdentityKey(bytearray(self.sessionStructure.pendingKeyExchange\
                                                            .localIdentityKey), 0)

        privateKey = Curve.decodePrivatePoint(self.sessionStructure.pendingKeyExchange.localIdentityKeyPrivate)
        return IdentityKeyPair(publicKey, privateKey)

    def hasPendingKeyExchange(self):
        return self.sessionStructure.HasField("pendingKeyExchange")


    def setUnacknowledgedPreKeyMessage(self, preKeyId, signedPreKeyId, baseKey):
        """
        :type preKeyId: int
        :type signedPreKeyId: int
        :type baseKey: ECPublicKey
        """

        self.sessionStructure.pendingPreKey.signedPreKeyId = signedPreKeyId
        self.sessionStructure.pendingPreKey.baseKey = baseKey.serialize()

        if preKeyId is not None:
            self.sessionStructure.pendingPreKey.preKeyId = preKeyId

    def hasUnacknowledgedPreKeyMessage(self):
        return self.sessionStructure.HasField("pendingPreKey")

    def getUnacknowledgedPreKeyMessageItems(self):
        preKeyId = None
        if self.sessionStructure.pendingPreKey.HasField("preKeyId"):
            preKeyId = self.sessionStructure.pendingPreKey.preKeyId

        return SessionState.UnacknowledgedPreKeyMessageItems(preKeyId,
                                     self.sessionStructure.pendingPreKey.signedPreKeyId,
                                     Curve.decodePoint(bytearray(self.sessionStructure.pendingPreKey\
                                                                 .baseKey), 0))
    def clearUnacknowledgedPreKeyMessage(self):
        self.sessionStructure.ClearField("pendingPreKey")

    def setRemoteRegistrationId(self, registrationId):
        self.sessionStructure.remoteRegistrationId = registrationId

    def getRemoteRegistrationId(self, registrationId):
        return self.sessionStructure.remoteRegistrationId

    def setLocalRegistrationId(self, registrationId):
        self.sessionStructure.localRegistrationId = registrationId

    def getLocalRegistrationId(self):
        return self.sessionStructure.localRegistrationId

    def serialize(self):
        return self.sessionStructure.SerializeToString()


    class UnacknowledgedPreKeyMessageItems:
        def __init__(self, preKeyId, signedPreKeyId, baseKey):
            """
            :type preKeyId: int
            :type signedPreKeyId: int
            :type baseKey: ECPublicKey
            """
            self.preKeyId       = preKeyId
            self.signedPreKeyId = signedPreKeyId
            self.baseKey        = baseKey


        def getPreKeyId(self):
            return self.preKeyId

        def getSignedPreKeyId(self):
            return self.signedPreKeyId

        def getBaseKey(self):
            return self.baseKey

