import storageprotos
from ..identitykey import IdentityKey
from ..ratchet.rootkey import RootKey
from ..kdf.hkdf import HKDF
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from ..ratchet.chainkey import ChainKey
from ..kdf.messagekeys import MessageKeys
class SessionState:
    def __init__(self, sessionStructure = None):
        self.sessionStructure = sessionStructure or storageprotos.SessionStructure()

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
        self.sessionStructure.localIdentityPublik = identityKey.serialize()


    def getRemoteIdentityKey(self):
        if self.sessionStructure.removeIdentityPublic is None:
            return None
        return IdentityKey(self.sessionStructure.remoteIdentityPublic)

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
        return self.sessionStructure.senderChain is not None

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
                        receiverChain.getChainKey().getKey(),
                        receiverChain.getChainKey().getIndex())

    def addReceiverChain(self, ECPublickKey_senderRatchetKey, chainKey):
        senderRatchetKey = ECPublickKey_senderRatchetKey

        chainKeyStructure = storageprotos.SessionStructure.Chain.ChainKey()
        chainKeyStructure.key = chainKey.getKey()
        chainKeyStructure.index = chainKey.getIndex()

        chain = storageprotos.SessionStructure.Chain()
        chain.key = chainKeyStructure
        chain.senderRatchetKey = senderRatchetKey.serialize()

        self.sessionStructure.receiverChains.append(chain)

        if len(self.sessionStructure.receiverChains) > 5:
            self.sessionStructure.receiverChains.pop(0)


    def setSenderChain(self, ECKeyPair_senderRatchetKeyPair, chainKey):
        senderRatchetKeyPair = ECKeyPair_senderRatchetKeyPair
        chainKeyStructure = storageprotos.SessionStructure.Chain.ChainKey()
        chainKeyStructure.key = chainKey.key
        chainKeyStructure.index = chainKey.index

        senderChain = storageprotos.SessionStructure.Chain()
        senderChain.senderRatchetKey = senderRatchetKeyPair.getPublickKey().serialize()
        senderChain.senderRatchetKeyPrivate = senderRatchetKeyPair.getPrivateKey().serialize()
        senderChain.chainKey = chainKeyStructure

        self.sessionStructure.senderChain = senderChain


    def getSenderChainKey(self):
        chainKeyStructure = self.sessionStructure.senderChain.chainKey
        return ChainKey(HKDF.createFor(self.getSessionVersion()),
                        chainKeyStructure.key, chainKeyStructure.index)

    def setSenderChainKey(self, ChainKey_nextChainKey):
        nextChainKey = ChainKey
        chainKey = storageprotos.SessionStructure.Chain.ChainKey()
        chainKey.key = nextChainKey.getKey()
        chainKey.index = nextChainKey.getIndex()
        chain = self.sessionStructure.Chain()
        chain.chainKey = chainKey
        self.sessionStructure.senderChain = chain


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
                messageKeyList.pop(i)
                break

        updatedChain = chain
        updatedChain.messageKeys = messageKeyList
        self.sessionStructure.receiverChains[chainAndIndex[1]] = updatedChain

        return result

    def setMessageKeys(self, ECPublicKey_senderEphemeral, messageKeys):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        messageKeyStructure = storageprotos.SessionStructure.Chain.MessageKey()
        messageKeyStructure.cipherKey = messageKeys.getCipherKey()
        messageKeyStructure.macKey = messageKeys.getMacKey()
        messageKeyStructure.index = messageKeys.getCounter()
        messageKeyStructure.iv = messageKeys.getIv()


        chain.messageKeys.append(messageKeyStructure)

        self.sessionStructure.receiverChains[chainAndIndex[1]] = chain


    def setReceiverChainKey(self, ECPublicKey_senderEphemeral, chainKey):
        senderEphemeral = ECPublicKey_senderEphemeral
        chainAndIndex = self.getReceiverChain(senderEphemeral)
        chain = chainAndIndex[0]
        chainKeyStructure = storageprotos.SessionStructure.Chain.ChainKey()
        chainKeyStructure.key = chainKey.getKey()
        chainKeyStructure.index = chainKey.getIndex()

        chain.chainkey = chainKeyStructure
        self.sessionStructure.receiverChains[chainAndIndex[1]] = chain



