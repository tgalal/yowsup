from ecc.curve import Curve
import Crypto.Cipher.AES as AES
from Crypto.Util import Counter
from ratchet.chainkey import ChainKey
from .sessionbuilder import SessionBuilder
from util.byteutil import ByteUtil
from .state.sessionstate import SessionState
import struct
class SessionCipher:


    def __init__(self, sessionStore, preKeyStore, signedPreKeyStore, identityKeyStore, recepientId, deviceId):
        self.sessionStore = sessionStore
        self.preKeyStore = preKeyStore
        self.recepientId = recepientId
        self.deviceId = deviceId
        self.sessionBuilder = SessionBuilder(sessionStore, preKeyStore, signedPreKeyStore,
                                             identityKeyStore, recepientId, deviceId)



    """
  public byte[] decrypt(PreKeyWhisperMessage ciphertext, DecryptionCallback callback)
      throws DuplicateMessageException, LegacyMessageException, InvalidMessageException,
             InvalidKeyIdException, InvalidKeyException, UntrustedIdentityException
  {
    synchronized (SESSION_LOCK) {
      SessionRecord     sessionRecord    = sessionStore.loadSession(recipientId, deviceId);
      Optional<Integer> unsignedPreKeyId = sessionBuilder.process(sessionRecord, ciphertext);
      byte[]            plaintext        = decrypt(sessionRecord, ciphertext.getWhisperMessage());

      callback.handlePlaintext(plaintext);

      sessionStore.storeSession(recipientId, deviceId, sessionRecord);

      if (unsignedPreKeyId.isPresent()) {
        preKeyStore.removePreKey(unsignedPreKeyId.get());
      }

      return plaintext;
    }
  }
    """

    def decryptPkmsg(self, ciphertext):
        """
        :type ciphertext: PreKeyWhisperMessage
        """
        sessionRecord = self.sessionStore.loadSession(self.recepientId, self.deviceId)
        unsigedPreKeyId = self.sessionBuilder.process(sessionRecord, ciphertext)
        plaintext = self.decryptWithSessionRecord(sessionRecord, ciphertext.getWhisperMessage())

        #callback.handlePlaintext(plaintext);
        self.sessionStore.storeSession(unsigedPreKeyId)

        if unsigedPreKeyId is not None:
            self.preKeyStore.removePreKey(unsigedPreKeyId)

        return plaintext


    def decryptWithSessionRecord(self, sessionRecord, cipherText):
        """
        :type sessionRecord: SessionRecord
        :type cipherText: WhisperMessage
        """

        previousStates = sessionRecord.getPreviousSessionStates()
        sessionState = SessionState(sessionRecord.getSessionState())
        plaintext = self.decryptWithSessionState(sessionState, cipherText)
        sessionRecord.setState(sessionState)

        return plaintext


    """
      private byte[] decrypt(SessionRecord sessionRecord, WhisperMessage ciphertext)
      throws DuplicateMessageException, LegacyMessageException, InvalidMessageException
  {
    synchronized (SESSION_LOCK) {
      Iterator<SessionState> previousStates = sessionRecord.getPreviousSessionStates().iterator();
      List<Exception>        exceptions     = new LinkedList<>();

      try {
        SessionState sessionState = new SessionState(sessionRecord.getSessionState());
        byte[]       plaintext    = decrypt(sessionState, ciphertext);

        sessionRecord.setState(sessionState);
        return plaintext;
      } catch (InvalidMessageException e) {
        exceptions.add(e);
      }

      while (previousStates.hasNext()) {
        try {
          SessionState promotedState = new SessionState(previousStates.next());
          byte[]       plaintext     = decrypt(promotedState, ciphertext);

          previousStates.remove();
          sessionRecord.promoteState(promotedState);

          return plaintext;
        } catch (InvalidMessageException e) {
          exceptions.add(e);
        }
      }

      throw new InvalidMessageException("No valid sessions.", exceptions);
    }
  }
    """

    def decryptWithSessionState(self, sessionState, ciphertextMessage):

        if not sessionState.hasSenderChain():
            raise Exception("Uninitialized session!")

        if ciphertextMessage.getMessageVersion() != sessionState.getSessionVersion():
            raise Exception("Message version %s, but session version %s" % (ciphertextMessage.getMessageVersion,
                                                                            sessionState.getSessionVersion()))

        messageVersion = ciphertextMessage.getMessageVersion()
        theirEphemeral = ciphertextMessage.getSenderRatchetKey()
        counter           = ciphertextMessage.getCounter()
        chainKey          = self.getOrCreateChainKey(sessionState, theirEphemeral)
        messageKeys       = self.getOrCreateMessageKeys(sessionState, theirEphemeral,
                                                              chainKey, counter)

        ciphertextMessage.verifyMac(messageVersion,
                                    sessionState.getRemoteIdentityKey(),
                                    sessionState.getLocalIdentityKey(),
                                    messageKeys.getMacKey())

        plaintext = self.getPlaintext(messageVersion, messageKeys, ciphertextMessage.getBody())
        #sessionState.clearUnacknowledgedPreKeyMessage();

        return plaintext


    def getOrCreateChainKey(self, sessionState, ECPublickKey_theirEphemeral):
        theirEphemeral = ECPublickKey_theirEphemeral
        if sessionState.hasReceiverChain(theirEphemeral):
            return sessionState.getReceiverChainKey(theirEphemeral)
        else:
            rootKey = sessionState.getRootKey()
            ourEphemeral = sessionState.getSenderRatchetKeyPair()
            receiverChain = rootKey.createChain(theirEphemeral, ourEphemeral)
            ourNewEphemeral = Curve.generateKeyPair()
            senderChain = receiverChain[0].createChain(theirEphemeral, ourNewEphemeral)

            sessionState.setRootKey(senderChain[0])
            sessionState.addReceiverChain(theirEphemeral, receiverChain[1])
            sessionState.setPreviousCounter(max(sessionState.getSenderChainKey().getIndex() - 1, 0))
            sessionState.setSenderChain(ourNewEphemeral, senderChain[1])
            return receiverChain[1]

    def getOrCreateMessageKeys(self, sessionState, ECPublicKey_theirEphemeral, chainKey, counter):
        theirEphemeral = ECPublicKey_theirEphemeral
        if chainKey.getIndex() > counter:
            if sessionState.hasMessageKeys(theirEphemeral, counter):
                return sessionState.removeMessageKeys(theirEphemeral, counter)
            else:
                raise Exception("Duplicate Message Exception, Received message "
                                "with old counter: %s, %s" % chainKey.getIndex(), counter)

        if counter - chainKey.getIndex > 2000:
            raise Exception("InvalidMessageException, Over 2000 messages into the future!")

        while chainKey.getIndex < counter:
            messageKeys = chainKey.getMessageKeys()
            sessionState.setMessageKeys(theirEphemeral, messageKeys)
            chainKey = chainKey.getNextChainKey()

        sessionState.setReceiverChainKey(theirEphemeral, chainKey.getNextChainKey())
        return chainKey.getMessageKeys()


    def getPlaintext(self, version, messageKeys, cipherText):
        cipher = None
        if version >= 3:
           cipher = self.getCipher(messageKeys.getCipherKey(), messageKeys.getIv())
        else:
            cipher = self.getCipher_v2(messageKeys.getCipherKey(), messageKeys.getCounter())

        return cipher.decrypt(cipherText)


    def getCipher(self, key, iv):
        #Cipher.getInstance("AES/CBC/PKCS5Padding");
        cipher = AES.new(key, AES.MODE_CBC, IV = iv)
        return cipher


    def getCipher_v2(self, key, counter):
        #AES/CTR/NoPadding
        counterbytes = struct.pack('>L', counter) + (b'\x00' * 12)
        counterint = int.from_bytes(counterbytes, byteorder='big')
        ctr=Counter.new(128, initial_value=counterint)

        #cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
        ivBytes = bytearray(16)
        ByteUtil.intToByteArray(ivBytes, 0, counter)

        cipher = AES.new(key, AES.MODE_CTR, IV = ivBytes)

        return cipher


