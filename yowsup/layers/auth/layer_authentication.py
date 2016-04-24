from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent, YowProtocolLayer, EventCallback
from .keystream import KeyStream
from yowsup.common.tools import TimeTools
from .layer_crypt import YowCryptLayer
from yowsup.layers.network import YowNetworkLayer
from .autherror import AuthError
from .protocolentities import *
from yowsup.common.tools import StorageTools
from yowsup.env import YowsupEnv
from .layer_interface_authentication import YowAuthenticationProtocolLayerInterface
from .protocolentities import StreamErrorProtocolEntity
import base64

class YowAuthenticationProtocolLayer(YowProtocolLayer):
    EVENT_LOGIN      = "org.openwhatsapp.yowsup.event.auth.login"
    EVENT_AUTHED  = "org.openwhatsapp.yowsup.event.auth.authed"
    PROP_CREDENTIALS = "org.openwhatsapp.yowsup.prop.auth.credentials"
    PROP_PASSIVE = "org.openwhatsapp.yowsup.prop.auth.passive"

    def __init__(self):
        handleMap = {
            "stream:features": (self.handleStreamFeatures, None),
            "failure": (self.handleFailure, None),
            "success": (self.handleSuccess, None),
            "challenge": (self.handleChallenge, None),
            "stream:error": (self.handleStreamError, None),
        }
        super(YowAuthenticationProtocolLayer, self).__init__(handleMap)
        self.interface = YowAuthenticationProtocolLayerInterface(self)
        self.credentials = None #left for backwards-compat
        self._credentials = None #new style set

    def __str__(self):
        return "Authentication Layer"

    def __getCredentials(self, credentials = None):
        u, pb64 = credentials or self.getProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS)
        if type(pb64) is str:
            pb64 = pb64.encode()
        password = base64.b64decode(pb64)
        return (u, bytearray(password))

    def setCredentials(self, credentials):
        self.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials) #keep for now
        self._credentials = self.__getCredentials(credentials)

    def getUsername(self, full = False):
        if self._credentials:
            return self._credentials[0] if not full else ("%s@%s" % (self._credentials[0], YowConstants.WHATSAPP_SERVER))
        else:
            prop = self.getProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS)
            return prop[0] if prop else None

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, yowLayerEvent):
        self.login()

    ## general methods
    def login(self):
        self.credentials = self._credentials or self.__getCredentials()
        self._sendFeatures()
        self._sendAuth()

    ###recieved node handlers handlers
    def handleStreamFeatures(self, node):
        nodeEntity = StreamFeaturesProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)

    def handleSuccess(self, node):
        if(node.data != None): StorageTools.writeNonce(self.credentials[0],node.data)
        successEvent = YowLayerEvent(self.__class__.EVENT_AUTHED, passive = self.getProp(self.__class__.PROP_PASSIVE))
        self.broadcastEvent(successEvent)
        nodeEntity = SuccessProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)

    def handleFailure(self, node):
        nodeEntity = FailureProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)
        self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT, reason = "Authentication Failure"))
        raise AuthError(nodeEntity.getReason())

    def handleChallenge(self, node):
        nodeEntity = ChallengeProtocolEntity.fromProtocolTreeNode(node)
        self._sendResponse(nodeEntity.getNonce())

    def handleStreamError(self, node):
        nodeEntity = StreamErrorProtocolEntity.fromProtocolTreeNode(node)
        errorType = nodeEntity.getErrorType()

        if not errorType:
            raise AuthError("Unhandled stream:error node:\n%s" % node)

        self.toUpper(nodeEntity)

    ##senders
    def _sendFeatures(self):
        self.entityToLower(StreamFeaturesProtocolEntity([]))

    def _sendAuth(self):
        passive = self.getProp(self.__class__.PROP_PASSIVE, False)
        nonce = StorageTools.getNonce(self.credentials[0])

        if nonce == None:
            self.entityToLower(AuthProtocolEntity(self.credentials[0], passive=passive))
        else:
            inputKey, outputKey, authBlob = self.generateAuthBlob(nonce)
            #to prevent enr whole response
            self.broadcastEvent(YowLayerEvent(YowCryptLayer.EVENT_KEYS_READY, keys = (inputKey, None)))
            self.entityToLower(AuthProtocolEntity(self.credentials[0], passive=passive, nonce=authBlob))
            self.broadcastEvent(YowLayerEvent(YowCryptLayer.EVENT_KEYS_READY, keys = (inputKey, outputKey)))


    def _sendResponse(self,nonce):
        inputKey, outputKey, authBlob = self.generateAuthBlob(nonce)
        responseEntity = ResponseProtocolEntity(authBlob)

        #to prevent enr whole response
        self.broadcastEvent(YowLayerEvent(YowCryptLayer.EVENT_KEYS_READY, keys = (inputKey, None)))
        self.entityToLower(responseEntity)
        self.broadcastEvent(YowLayerEvent(YowCryptLayer.EVENT_KEYS_READY, keys = (inputKey, outputKey)))
        #YowCryptLayer.setProp("outputKey", outputKey)


    def generateAuthBlob(self, nonce):
        keys = KeyStream.generateKeys(self.credentials[1], nonce)
        currentEnv = YowsupEnv.getCurrent()

        inputKey = KeyStream(keys[2], keys[3])
        outputKey = KeyStream(keys[0], keys[1])

        #YowCryptLayer.setProp("inputKey", inputKey)


        nums = bytearray(4)

        #nums = [0] * 4


        username_bytes = list(map(ord, self.credentials[0]))
        nums.extend(username_bytes)
        nums.extend(nonce)

        utcNow = str(int(TimeTools.utcTimestamp()))
        time_bytes =  list(map(ord, utcNow))
        nums.extend(time_bytes)

        strCat = "\x00\x00\x00\x00\x00\x00\x00\x00"
        strCat += currentEnv.getOSVersion() + "\x00"
        strCat += currentEnv.getManufacturer() + "\x00"
        strCat += currentEnv.getDeviceName() + "\x00"
        strCat += currentEnv.getBuildVersion()
        nums.extend(list(map(ord, strCat)))

        encoded = outputKey.encodeMessage(nums, 0, 4, len(nums) - 4)
        authBlob = "".join(map(chr, encoded))

        return (inputKey, outputKey, authBlob)
