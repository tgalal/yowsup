from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from Yowsup import ProtocolTreeNode
from keystream import KeyStream
from watime import WATime
from crypt import YowCryptLayer
from autherror import AuthError
from protocolentities import *
class YowAuthenticatorLayer(YowProtocolLayer):
    STATE_AUTHED    = 0
    STATE_NOAUTH    = 1
    def __init__(self):
        handleMap = {
            "stream:features": self.handleStreamFeatures,
            "failure": self.handleFailure,
            "success": self.handleSuccess,
            "challenge": self.handleChallenge
        }
        super(YowAuthenticatorLayer, self).__init__(handleMap)
        self.supportsReceiptAcks = False
        self.state = YowAuthenticatorLayer.STATE_NOAUTH 

    # def init(self):
    #     self.sendFeatures()
    #     self.sendAuth();
    #     self.initUpper()
    #     return True


    def onEvent(self, event):
        if event.getName() == "network.state.connected":
            self.sendFeatures()
            self.sendAuth();

    def sendFeatures(self):
        self.entityToLower(StreamFeaturesProtocolEntity())

    def entityToLower(self, protocolentity):
        self.toLower(protocolentity.toProtocolTreeNode())

    def sendAuth(self):
        self.entityToLower(AuthProtocolEntity(YowAuthenticatorLayer.getProp("credentials")[0]))

    def send(self, data):
        self.entityToLower(data)

    def handleStreamFeatures(self, node):
        nodeEntity = StreamFeaturesProtocolEntity.fromProtocolTreeNode(node)
        self.supportsReceiptAcks  = nodeEntity.supportsReceiptAcks()

    def handleSuccess(self, node):
        self.state = YowAuthenticatorLayer.STATE_AUTHED

    def handleFailure(self, node):
        raise AuthError("Authentication failed")

    def handleChallenge(self, node):
        nodeEntity = ChallengeProtocolEntity.fromProtocolTreeNode(node)
        self.sendResponse(nodeEntity.getNonce())

    def processSuccessNode(self, node):
        self.state = YowAuthenticatorLayer.STATE_AUTHED

    def sendResponse(self,nonce):
        keys = KeyStream.generateKeys(YowAuthenticatorLayer.getProp("credentials")[1], nonce)

        inputKey = KeyStream(keys[2], keys[3])
        outputKey = KeyStream(keys[0], keys[1])

        YowCryptLayer.setProp("inputKey", inputKey)

        nums = [0] * 4

        nums.extend(YowAuthenticatorLayer.getProp("credentials")[0])
        nums.extend(nonce)

        wt = WATime()
        utcNow = int(wt.utcTimestamp())
        nums.extend(str(utcNow))

        encoded = outputKey.encodeMessage(nums, 0, 4, len(nums) - 4)
        authBlob = "".join(map(chr, encoded))


        responseEntity = ResponseProtocolEntity(authBlob)
        self.entityToLower(responseEntity)
        YowCryptLayer.setProp("outputKey", outputKey)

    def __str__(self):
        return "Autheticator Layer"


