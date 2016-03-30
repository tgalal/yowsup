from yowsup.layers import YowProtocolLayer, YowLayerEvent, EventCallback
from .protocolentities import SetKeysIqProtocolEntity
from axolotl.util.keyhelper import KeyHelper
from .store.sqlite.liteaxolotlstore import LiteAxolotlStore
from axolotl.sessionbuilder import SessionBuilder
from yowsup.layers.protocol_messages.protocolentities.message import MessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from axolotl.ecc.curve import Curve
from yowsup.common.tools import StorageTools
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.protocol.whispermessage import WhisperMessage
from .protocolentities import EncryptedMessageProtocolEntity
from axolotl.sessioncipher import SessionCipher
from yowsup.structs import ProtocolTreeNode
from .protocolentities import GetKeysIqProtocolEntity, ResultGetKeysIqProtocolEntity
from axolotl.util.hexutil import HexUtil
from axolotl.invalidmessageexception import InvalidMessageException
from axolotl.duplicatemessagexception import DuplicateMessageException
from .protocolentities import EncryptNotification
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from axolotl.invalidkeyidexception import InvalidKeyIdException
from axolotl.nosessionexception import NoSessionException
from axolotl.untrustedidentityexception import UntrustedIdentityException
from .protocolentities.receipt_outgoing_retry import RetryOutgoingReceiptProtocolEntity
from yowsup.common import YowConstants
import binascii
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
        if node.tag == "message" and node["type"] == "text" and node["to"] not in self.skipEncJids and not YowConstants.WHATSAPP_GROUP_SERVER in node["to"]:
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
                EncryptedMessageProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncryptedMessageProtocolEntity.TYPE_PKMSG ,
                                                   version,
                                                   ciphertext.serialize(),
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
        try:
            if node.getChild("enc")["v"] == "2" and node["from"] not in self.v2Jids:
                self.v2Jids.append(node["from"])

            if node.getChild("enc")["type"] == "pkmsg":
                self.handlePreKeyWhisperMessage(node)
            else:
                self.handleWhisperMessage(node)
        except InvalidMessageException as e:
            # logger.error("Invalid message from %s!! Your axololtl database data might be inconsistent with WhatsApp, or with what that contact has" % node["from"])
            # sys.exit(1)
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMesageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except InvalidKeyIdException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMesageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())
        except NoSessionException as e:
            logger.error(e)
            entity = GetKeysIqProtocolEntity([node["from"]])
            if node["from"] not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[node["from"]] = []
            self.pendingIncomingMessages[node["from"]].append(node)

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

        preKeyWhisperMessage = PreKeyWhisperMessage(serialized=pkMessageProtocolEntity.getEncData())
        sessionCipher = self.getSessionCipher(pkMessageProtocolEntity.getFrom(False))
        plaintext = sessionCipher.decryptPkmsg(preKeyWhisperMessage)

        if pkMessageProtocolEntity.getVersion() == 2:
            plaintext = self.unpadV2Plaintext(plaintext)


        bodyNode = ProtocolTreeNode("body", data = plaintext)
        node.addChild(bodyNode)
        self.toUpper(node)

    def handleWhisperMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)

        whisperMessage = WhisperMessage(serialized=encMessageProtocolEntity.getEncData())
        sessionCipher = self.getSessionCipher(encMessageProtocolEntity.getFrom(False))
        plaintext = sessionCipher.decryptMsg(whisperMessage)

        if encMessageProtocolEntity.getVersion() == 2:
            plaintext = self.unpadV2Plaintext(plaintext)

        bodyNode = ProtocolTreeNode("body", data = plaintext)
        node.addChild(bodyNode)
        self.toUpper(node)

    def unpadV2Plaintext(self, v2plaintext):
        if len(v2plaintext) < 128:
            return v2plaintext[2:-1]
        else: # < 128 * 128
            return v2plaintext[3: -1]

    ####

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
            return self.sessionCiphers[recipientId]
        else:
            self.sessionCiphers[recipientId] = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            return self.sessionCiphers[recipientId]
