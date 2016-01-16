from yowsup.layers import YowProtocolLayer, YowLayerEvent, EventCallback
from yowsup.layers.protocol_messages.protocolentities.message import MessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.axolotl.e2e_pb2 import Message
from yowsup.layers.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode
from yowsup.common.tools import StorageTools

from axolotl.sessionbuilder import SessionBuilder
from axolotl.util.keyhelper import KeyHelper
from axolotl.ecc.curve import Curve
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.protocol.senderkeymessage import SenderKeyMessage
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.util.hexutil import HexUtil
from axolotl.invalidmessageexception import InvalidMessageException
from axolotl.duplicatemessagexception import DuplicateMessageException
from axolotl.invalidkeyidexception import InvalidKeyIdException
from axolotl.nosessionexception import NoSessionException
from axolotl.untrustedidentityexception import UntrustedIdentityException
from axolotl.axolotladdress import AxolotlAddress
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from axolotl.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage

import binascii
import copy
import sys
import logging

logger = logging.getLogger(__name__)

class YowAxolotlLayer(YowProtocolLayer):
    EVENT_PREKEYS_SET = "org.openwhatsapp.yowsup.events.axololt.setkeys"
    _STATE_INIT = 0
    _STATE_GENKEYS = 1
    _STATE_HASKEYS = 2
    _COUNT_PREKEYS = 200
    _DB = "axolotl.db"

    def __init__(self):
        super(YowAxolotlLayer, self).__init__()
        self.store = None
        self.state = self.__class__._STATE_INIT

        self.sessionCiphers = {}
        self.groupCiphers = {}
        self.pendingMessages = {}
        self.pendingIncomingMessages = {}
        self.skipEncJids = []
        self.v2Jids = [] #people we're going to send v2 enc messages

    @property
    def store(self):
        if self._store is None:
            self.store = LiteAxolotlStore(
                StorageTools.constructPath(
                    self.getProp(
                        YowAuthenticationProtocolLayer.PROP_CREDENTIALS)[0],
                    self.__class__._DB
                )
            )
            self.state = self.__class__._STATE_HASKEYS if  self.store.getLocalRegistrationId() is not None \
                else self.__class__._STATE_INIT

        return self._store

    @store.setter
    def store(self, store):
        self._store = store

    def __str__(self):
        return "Axolotl Layer"

    ### store and state


    def isInitState(self):
        return self.store == None or self.state == self.__class__._STATE_INIT

    def isGenKeysState(self):
        return self.state == self.__class__._STATE_GENKEYS
    ########


    @EventCallback(EVENT_PREKEYS_SET)
    def onPreKeysSet(self, yowLayerEvent):
        self.sendKeys(fresh=False)

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, yowLayerEvent):
        if self.isInitState():
            self.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)

    @EventCallback(YowAuthenticationProtocolLayer.EVENT_AUTHED)
    def onAuthed(self, yowLayerEvent):
        if yowLayerEvent.getArg("passive") and self.isInitState():
            logger.info("Axolotl layer is generating keys")
            self.sendKeys()

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onDisconnected(self, yowLayerEvent):
        if self.isGenKeysState():
            #we requested this disconnect in this layer to switch off passive
            #no need to traverse it to upper layers?
            self.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, False)
            self.state = self.__class__._STATE_HASKEYS
            self.getLayerInterface(YowNetworkLayer).connect()
        else:
            self.store = None

    def send(self, node):
        if node.tag == "message" and node["type"] == "text" and node["to"] not in self.skipEncJids:
            self.handlePlaintextNode(node)
            return
        self.toLower(node)

    def receive(self, protocolTreeNode):
        """
        :type protocolTreeNode: ProtocolTreeNode
        """
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "message":
                self.onMessage(protocolTreeNode)
                return
            elif protocolTreeNode.tag == "notification" and protocolTreeNode["type"] == "encrypt":
                self.onEncryptNotification(protocolTreeNode)
                return
            elif protocolTreeNode.tag == "receipt" and protocolTreeNode["type"] == "retry":
                # should bring up that message, resend it, but in upper layer?
                # as it might have to be fetched from a persistent storage
                pass
            self.toUpper(protocolTreeNode)
    ######

    ##### handling received data #####
    def onEncryptNotification(self, protocolTreeNode):
        entity = EncryptNotification.fromProtocolTreeNode(protocolTreeNode)
        ack = OutgoingAckProtocolEntity(protocolTreeNode["id"], "notification", protocolTreeNode["type"], protocolTreeNode["from"])
        self.toLower(ack.toProtocolTreeNode())
        self.sendKeys(fresh=False, countPreKeys = self.__class__._COUNT_PREKEYS - entity.getCount())

    def onMessage(self, protocolTreeNode):
        encNode = protocolTreeNode.getChild("enc")
        if encNode:
            self.handleEncMessage(protocolTreeNode)
        else:
            self.toUpper(protocolTreeNode)

    ####

    def processPendingMessages(self, jid):
        if jid in self.pendingMessages:
            for messageNode in self.pendingMessages[jid]:
                if jid in self.skipEncJids:
                    self.toLower(messageNode)
                else:
                    self.handlePlaintextNode(messageNode)

            del self.pendingMessages[jid]

    def processPendingIncomingMessages(self, jid):
        if jid in self.pendingIncomingMessages:
            for messageNode in self.pendingIncomingMessages[jid]:
                self.onMessage(messageNode)

            del self.pendingIncomingMessages[jid]

    #### handling message types

    def handlePlaintextNode(self, node):
        plaintext = node.getChild("body").getData()
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        recipient_id = entity.getTo(False)

        if not self.store.containsSession(recipient_id, 1):
            entity = GetKeysIqProtocolEntity([node["to"]])
            if node["to"] not in self.pendingMessages:
                self.pendingMessages[node["to"]] = []
            self.pendingMessages[node["to"]].append(node)

            self._sendIq(entity, lambda a, b: self.onGetKeysResult(a, b, self.processPendingMessages), self.onGetKeysError)
        else:

            sessionCipher = self.getSessionCipher(recipient_id)

            if node["to"] in self.v2Jids:
                version = 2
                padded = bytearray()
                padded.append(ord("\n"))
                padded.extend(self.encodeInt7bit(len(plaintext)))
                padded.extend(plaintext)
                padded.append(ord("\x01"))
                plaintext = padded
            else:
                version = 1
            ciphertext = sessionCipher.encrypt(plaintext)
            encEntity = EncryptedMessageProtocolEntity(
                [
                    EncProtocolEntity(EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG ,
                                                   version,
                                                   ciphertext.serialize())],
                                                   MessageProtocolEntity.MESSAGE_TYPE_TEXT,
                                                   _id= node["id"],
                                                   to = node["to"],
                                                   notify = node["notify"],
                                                   timestamp= node["timestamp"],
                                                   participant=node["participant"],
                                                   offline=node["offline"],
                                                   retry=node["retry"]
                                                   )
            self.toLower(encEntity.toProtocolTreeNode())

    def encodeInt7bit(self, value):
        v = value
        out = bytearray()
        while v >= 0x80:
          out.append((v | 0x80) % 256)
          v >>= 7
        out.append(v % 256)

        return out

    def handleEncMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        isGroup = node["from"] if node["participant"] is None else node["from"]
        senderJid = node["participant"] if isGroup else node["from"]
        encNode = None
        if node.getChild("enc")["v"] == "2" and senderJid not in self.v2Jids:
            self.v2Jids.append(senderJid)
        try:
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG):
                self.handlePreKeyWhisperMessage(node)
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG):
                self.handleWhisperMessage(node)
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG):
                self.handleSenderKeyMessage(node)
        except InvalidMessageException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except InvalidKeyIdException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except NoSessionException as e:
            logger.error(e)
            entity = GetKeysIqProtocolEntity([senderJid])
            if senderJid not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[senderJid] = []
            self.pendingIncomingMessages[senderJid].append(node)

            self._sendIq(entity, lambda a, b: self.onGetKeysResult(a, b, self.processPendingIncomingMessages), self.onGetKeysError)
        except DuplicateMessageException as e:
            logger.error(e)
            logger.warning("Going to send the delivery receipt myself !")
            self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"]).toProtocolTreeNode())

        except UntrustedIdentityException as e:
            logger.error(e)
            logger.warning("Ignoring message with untrusted identity")

    def handlePreKeyWhisperMessage(self, node):
        pkMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = pkMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG)
        preKeyWhisperMessage = PreKeyWhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(pkMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptPkmsg(preKeyWhisperMessage)
        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(pkMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(node, plaintext)

    def handleWhisperMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)

        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG)
        whisperMessage = WhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(encMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptMsg(whisperMessage)

        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(encMessageProtocolEntity, plaintext)

    def handleSenderKeyMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG)

        senderKeyName = SenderKeyName(encMessageProtocolEntity.getFrom(True), AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 1))
        groupCipher = GroupCipher(self.store, senderKeyName)
        try:
            plaintext = groupCipher.decrypt(enc.getData())
            if plaintext:
                self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext)
        except NoSessionException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())

    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        node = encMessageProtocolEntity.toProtocolTreeNode()
        m = Message()
        try:
            m.ParseFromString(serializedData)
        except:
            print("DUMP:")
            print(serializedData)
            print([s for s in serializedData])
            print([ord(s) for s in serializedData])
            raise
        if not m or not serializedData:
            raise ValueError("Empty message")

        handled = False

        if m.senderKeyDistributionMessage is not None:
            axolotlAddress = AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 1)
            self.handleSenderKeyDistributionMessage(m.senderKeyDistributionMessage, axolotlAddress)
            handled = True
        if m.conversation is not None:
            self.handleConversationMessage(node, m.conversation)
            handled = True

        if not handled:
            print(m)
            raise ValueError("Unhandled")

        ##TODO other message types

    def handleSenderKeyDistributionMessage(self, senderKeyDistributionMessage, axolotlAddress):
        groupId = senderKeyDistributionMessage.groupId
        axolotlSenderKeyDistributionMessage = SenderKeyDistributionMessage(serialized=senderKeyDistributionMessage.axolotlSenderKeyDistributionMessage)
        groupSessionBuilder = GroupSessionBuilder(self.store)
        senderKeyName = SenderKeyName(groupId, axolotlAddress)
        groupSessionBuilder.process(senderKeyName, axolotlSenderKeyDistributionMessage)

    def handleConversationMessage(self, originalEncNode, text):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode.children = []
        messageNode.addChild(ProtocolTreeNode("body", data = text))
        self.toUpper(messageNode)

    ### keys set and get
    def sendKeys(self, fresh = True, countPreKeys = _COUNT_PREKEYS):
        identityKeyPair     = KeyHelper.generateIdentityKeyPair() if fresh else self.store.getIdentityKeyPair()
        registrationId      = KeyHelper.generateRegistrationId() if fresh else self.store.getLocalRegistrationId()
        preKeys             = KeyHelper.generatePreKeys(KeyHelper.getRandomSequence(), countPreKeys)
        signedPreKey        = KeyHelper.generateSignedPreKey(identityKeyPair, KeyHelper.getRandomSequence(65536))
        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))

        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, Curve.DJB_TYPE, self.adjustId(registrationId))

        onResult = lambda _, __: self.persistKeys(registrationId, identityKeyPair, preKeys, signedPreKey, fresh)
        self._sendIq(setKeysIq, onResult, self.onSentKeysError)

    def persistKeys(self, registrationId, identityKeyPair, preKeys, signedPreKey, fresh):
        total = len(preKeys)
        curr = 0
        prevPercentage = 0

        if fresh:
            self.store.storeLocalData(registrationId, identityKeyPair)
        self.store.storeSignedPreKey(signedPreKey.getId(), signedPreKey)

        for preKey in preKeys:
            self.store.storePreKey(preKey.getId(), preKey)
            curr += 1
            currPercentage = int((curr * 100) / total)
            if currPercentage == prevPercentage:
                continue
            prevPercentage = currPercentage
            #logger.debug("%s" % currPercentage + "%")
            sys.stdout.write("Storing prekeys %d%% \r" % (currPercentage))
            sys.stdout.flush()

        if fresh:
            self.state = self.__class__._STATE_GENKEYS
            self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))

    def onSentKeysError(self, errorNode, keysEntity):
        raise Exception("Sent keys were not accepted")

    def onGetKeysResult(self, resultNode, getKeysEntity, processPendingFn):
        entity = ResultGetKeysIqProtocolEntity.fromProtocolTreeNode(resultNode)

        resultJids = entity.getJids()
        for jid in getKeysEntity.getJids():

            if jid not in resultJids:
                self.skipEncJids.append(jid)
                self.processPendingMessages(jid)
                continue

            recipient_id = jid.split('@')[0]
            preKeyBundle = entity.getPreKeyBundleFor(jid)

            sessionBuilder = SessionBuilder(self.store, self.store, self.store,
                                               self.store, recipient_id, 1)
            sessionBuilder.processPreKeyBundle(preKeyBundle)

            processPendingFn(jid)

    def onGetKeysError(self, errorNode, getKeysEntity):
        pass
    ###


    def adjustArray(self, arr):
        return HexUtil.decodeHex(binascii.hexlify(arr))

    def adjustId(self, _id):
        _id = format(_id, 'x')
        zfiller = len(_id) if len(_id) % 2 == 0 else len(_id) + 1
        _id = _id.zfill(zfiller if zfiller > 6 else 6)
        # if len(_id) % 2:
        #     _id = "0" + _id
        return binascii.unhexlify(_id)

    def getSessionCipher(self, recipientId):
        if recipientId in self.sessionCiphers:
            sessionCipher = self.sessionCiphers[recipientId]
        else:
            sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            self.sessionCiphers[recipientId] = sessionCipher

        return sessionCipher

    def getGroupCipher(self, groupId, senderId):
        senderKeyName = SenderKeyName(groupId, AxolotlAddress(senderId, 1))
        if senderKeyName in self.groupCiphers:
            groupCipher = self.groupCiphers[senderKeyName]
        else:
            groupCipher = GroupCipher(self.store, senderKeyName)
            self.groupCiphers[senderKeyName] = groupCipher
        return groupCipher
