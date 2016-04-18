from .layer_base import AxolotlBaseLayer
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network.layer import YowNetworkLayer
from axolotl.util.keyhelper import KeyHelper
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from axolotl.util.hexutil import HexUtil
from axolotl.ecc.curve import Curve
import logging
import binascii
import sys

logger = logging.getLogger(__name__)

class AxolotlControlLayer(AxolotlBaseLayer):
    _STATE_INIT = 0
    _STATE_GENKEYS = 1
    _STATE_HASKEYS = 2
    _COUNT_PREKEYS = 200
    EVENT_PREKEYS_SET = "org.openwhatsapp.yowsup.events.axololt.setkeys"

    def __init__(self):
        super(AxolotlControlLayer, self).__init__()
        self.state = self.__class__._STATE_INIT

    def onNewStoreSet(self, store):
        super(AxolotlControlLayer, self).onNewStoreSet(store)
        if store is not None:
            self.state = self.__class__._STATE_HASKEYS if  store.getLocalRegistrationId() is not None \
                else self.__class__._STATE_INIT

    def send(self, node):
        self.toLower(node)

    def receive(self, protocolTreeNode):
        """
        :type protocolTreeNode: ProtocolTreeNode
        """
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "notification" and protocolTreeNode["type"] == "encrypt":
                self.onEncryptNotification(protocolTreeNode)
                return
            self.toUpper(protocolTreeNode)

    def isInitState(self):
        return self.store == None or self.state == self.__class__._STATE_INIT

    def isGenKeysState(self):
        return self.state == self.__class__._STATE_GENKEYS


    def onEncryptNotification(self, protocolTreeNode):
        entity = EncryptNotification.fromProtocolTreeNode(protocolTreeNode)
        ack = OutgoingAckProtocolEntity(protocolTreeNode["id"], "notification", protocolTreeNode["type"], protocolTreeNode["from"])
        self.toLower(ack.toProtocolTreeNode())
        self.sendKeys(fresh=False, countPreKeys = self.__class__._COUNT_PREKEYS - entity.getCount())

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

    def adjustArray(self, arr):
        return HexUtil.decodeHex(binascii.hexlify(arr))

    def adjustId(self, _id):
        _id = format(_id, 'x')
        zfiller = len(_id) if len(_id) % 2 == 0 else len(_id) + 1
        _id = _id.zfill(zfiller if zfiller > 6 else 6)
        # if len(_id) % 2:
        #     _id = "0" + _id
        return binascii.unhexlify(_id)
