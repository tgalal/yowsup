from yowsup.layers.protocol_messages.protocolentities.test_message import MessageProtocolEntityTest
from yowsup.layers.textsecure.protocolentities import PkMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
#from yowsup.layers.textsecure.entities import ratcheting_session
#from yowsup.layers.textsecure.entities.prekeyrecord import PreKeyRecord
#from yowsup.layers.textsecure.pytextsecure.keyutils import IdentityKeyUtil
class PkMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(PkMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = PkMessageProtocolEntity
        encNode = ProtocolTreeNode("enc")
        encNode["type"] = "pkmsg"
        encNode["av"] = "Android/2.11.456"
        encNode["v"] = "1"
        serializedData = "330883b2c9031221059f00d22d0c9e3a7e91407bc43bbf91aa63381b8278e574e3337d01333972da101a" \
                         "210521f1a3f3d5cb87fde19fadf618d3001b64941715efd3e0f36bba48c23b08c82f2242330a2105aa80" \
                         "32436f334dc5f8d898c7660d59750ee370c27339a36b8b8c459ff3b2232610001800221038b1295976ba" \
                         "0e1e1ee700f04992720931a7236aa9009def28b99de8d2013000"
        encNode.setData(serializedData.decode('hex'))
        self.node.addChild(encNode)

    def test_pkproto(self):
        entity = PkMessageProtocolEntity.fromProtocolTreeNode(self.node)
        message = entity.getPkMessage()

        preKeyId = message.preKeyId
        theirBaseKey = message.baseKey
        theirEphemeralKey = message.message.senderEphemeral
        theirIdentityKey = message.identityKey


        # preKeyRecord = PreKeyRecord(preKeyId)
        # ourBaseKey = preKeyRecord.keyPair
        # ourEphemeralKey = ourBaseKey
        # ourIdentityKey = []#IdentityKeyUtil().getIdentityKeyPair()
        #
        # ratcheting_session.initializeSession(self.sessionRecord.sessionState,
        #                                      ourBaseKey, theirBaseKey,
        #                                      ourEphemeralKey, theirEphemeralKey,
        #                                      ourIdentityKey, theirIdentityKey)
        #
        # self.sessionRecord.sessionState.setLocalRegistrationId(123)
        # self.sessionRecord.sessionState.setRemoteRegistrationId(message.registrationId)
        #
        # #if simultaneousInitiate:
        # #    self.sessionRecord.getSessionState().setNeedsRefresh(True)
        #
        # self.sessionRecord.save()
        #
        #
        # recipient = incomingPushMessageSignal.source
        # recipientDevice = incomingPushMessageSignal.sourceDevice
        #
        # #if not SessionRecord().hasSession(recipientDevice):
        # #    sendResult(pushReceiver.RESULT_NO_SESSION)
        #
        # sessionCipher = session_cipher.SessionCipher(recipient)
        # plaintextBody = sessionCipher.decrypt(incomingPushMessageSignal.message)


        #initializeSessionAsBob(sessionState,
                           #ourBaseKey, theirBaseKey,
                           #ourEphemeralKey,
                           #ourIdentityKey, theirIdentityKey):

        # sessionState.setRemoteIdentityKey(theirIdentityKey)
        # sessionState.setLocalIdentityKey(ourIdentityKey.publicKey)
        #
        # sendingChain = calculate3DHE( False, ourBaseKey, theirBaseKey,
        #                          ourIdentityKey, theirIdentityKey)
        #
        # sessionState.setSenderChain( ourEphemeralKey, sendingChain[1] )
        # sessionState.setRootKey(sendingChain[0])


        # ciphertextMessage = entity.getPkMessage().mesage
        #
        # theirEphemeral = ciphertextMessage.senderEphemeral
        # counter = ciphertextMessage.counter
        # ourBaseKey = ratcheting_session.Curve().generateKeyPair(True)
        # ourEphemeralKey = ratcheting_session.Curve().generateKeyPair(True)
        # chainKey = ratcheting_session.RootKey(key).createChain(theirEphemeral, ourEphemeral)
        #
        # #self.getOrCreateChainKey(sessionState, theirEphemeral)
        # messageKeys = self.getOrCreateMessageKeys(sessionState, theirEphemeral,
        #                                      chainKey, counter)
        #
        # # TODO add methods?
        # ciphertextMessage.verifyMac(messageKeys.getMacKey())
        #
        # sessionState.sessionStructure.ClearField("pendingPreKey")
        # plaintext = self.getPlaintext(messageKeys, ciphertextMessage.ciphertext)


