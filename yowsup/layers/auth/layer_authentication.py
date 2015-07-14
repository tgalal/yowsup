from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .keystream import KeyStream
from yowsup.common.tools import TimeTools
from .layer_crypt import YowCryptLayer
from yowsup.layers.network import YowNetworkLayer
from .autherror import AuthError
from .protocolentities import *
from yowsup.common.tools import StorageTools
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
        self.credentials = None

    def __str__(self):
        return "Authentication Layer"

    def __getCredentials(self):
        u, pb64 = self.getProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS)
        if type(pb64) is str:
            pb64 = pb64.encode()
        password = base64.b64decode(pb64)
        return (u, bytearray(password))

    def onEvent(self, event):
        if event.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            self.login()
        elif event.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            self.credentials = self.__getCredentials()
            if not self.credentials:
                raise AuthError("Auth stopped connection signal as no credentials have been set")

    ## general methods
    def login(self):
        
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
        if node.getChild("text"):
            nodeEntity = StreamErrorConflictProtocolEntity.fromProtocolTreeNode(node)
        elif node.getChild("ack"):
            nodeEntity = StreamErrorAckProtocolEntity.fromProtocolTreeNode(node)
        else:
            raise AuthError("Unhandled stream:error node:\n%s" % node)
        self.toUpper(nodeEntity)

    ##senders
    def _sendFeatures(self):
        self.entityToLower(StreamFeaturesProtocolEntity(["readreceipts", "groups_v2", "privacy", "presence"]))

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

        encoded = outputKey.encodeMessage(nums, 0, 4, len(nums) - 4)
        authBlob = "".join(map(chr, encoded))

        return (inputKey, outputKey, authBlob)
