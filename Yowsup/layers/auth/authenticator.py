from Yowsup.layers import YowLayer
from Yowsup import ProtocolTreeNode
from keystream import KeyStream
from watime import WATime
from crypt import YowCryptLayer
from autherror import AuthError
class YowAuthenticatorLayer(YowLayer):
    STATE_AUTHED    = 0
    STATE_NOAUTH    = 1
    def __init__(self):
        YowLayer.__init__(self)
        self.supportsReceiptAcks = False
        self.state = YowAuthenticatorLayer.STATE_NOAUTH 

    def init(self):
        self.sendFeatures()
        self.sendAuth();
        self.initUpper()
        return True


    def toLower(self, data):
        YowLayer.toLower(self, ProtocolTreeNode(data[0], *data[1:]))


    def sendFeatures(self):
        self.toLower(("stream:features", None))


    def sendAuth(self):
        self.toLower(("auth", {"passive": "false", "mechanism": "WAUTH-2", "user": YowAuthenticatorLayer.getProp("credentials")[0]}))

    def send(self, data):
        self.toLower(data)

    def receive(self, node):

        if ProtocolTreeNode.tagEquals(node, "stream:features"):
            self.supportsReceiptAcks  = node.getChild("receipt_acks") is not None
        elif ProtocolTreeNode.tagEquals(node, "challenge"):
            challenge = node.data
            self.sendResponse(challenge)
        elif ProtocolTreeNode.tagEquals(node, "failure"):
            raise AuthError("Authentication failed")
        elif ProtocolTreeNode.tagEquals(node, "success"):
            self.processSuccessNode(node)
        elif self.state == YowAuthenticatorLayer.STATE_NOAUTH:
            raise AuthError("Failed to receive initial auth data")
        else:
            self.toUpper(node)

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

        node = ProtocolTreeNode("response",{"xmlns":"urn:ietf:params:xml:ns:xmpp-sasl"}, None, authBlob);
        self.toLower(("response", {"xmlns":"urn:ietf:params:xml:ns:xmpp-sasl"}, None, authBlob))
        YowCryptLayer.setProp("outputKey", outputKey)


