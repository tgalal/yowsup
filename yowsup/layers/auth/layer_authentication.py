from yowsup.common import YowConstants
from yowsup.layers import YowLayerEvent, YowProtocolLayer, EventCallback
from yowsup.layers.network import YowNetworkLayer
from .protocolentities import *
from .layer_interface_authentication import YowAuthenticationProtocolLayerInterface
from .protocolentities import StreamErrorProtocolEntity


class YowAuthenticationProtocolLayer(YowProtocolLayer):
    EVENT_AUTHED  = "org.openwhatsapp.yowsup.event.auth.authed"
    EVENT_AUTH = "org.openwhatsapp.yowsup.event.auth"
    PROP_CREDENTIALS = "org.openwhatsapp.yowsup.prop.auth.credentials"
    PROP_PASSIVE = "org.openwhatsapp.yowsup.prop.auth.passive"

    def __init__(self):
        handleMap = {
            "stream:features": (self.handleStreamFeatures, None),
            "failure": (self.handleFailure, None),
            "success": (self.handleSuccess, None),
            "stream:error": (self.handleStreamError, None),
        }
        super(YowAuthenticationProtocolLayer, self).__init__(handleMap)
        self.interface = YowAuthenticationProtocolLayerInterface(self)
        self.credentials = None #left for backwards-compat
        self._credentials = None #new style set

    def __str__(self):
        return "Authentication Layer"

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def on_connected(self, event):
        self.broadcastEvent(
            YowLayerEvent(
                self.EVENT_AUTH,
                credentials=self.getProp(self.PROP_CREDENTIALS),
                passive=self.getProp(self.PROP_PASSIVE, False)
            )
        )

    def setCredentials(self, credentials):
        self.setProp(self.PROP_CREDENTIALS, credentials) #keep for now
        self._credentials = credentials

#
    def getUsername(self, full = False):
        if self._credentials:
            return self._credentials[0] if not full else ("%s@%s" % (self._credentials[0], YowConstants.WHATSAPP_SERVER))
        else:
            prop = self.getProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS)
            return prop[0] if prop else None

    def handleStreamFeatures(self, node):
        nodeEntity = StreamFeaturesProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)

    def handleSuccess(self, node):
        successEvent = YowLayerEvent(self.__class__.EVENT_AUTHED, passive = self.getProp(self.__class__.PROP_PASSIVE))
        self.broadcastEvent(successEvent)
        nodeEntity = SuccessProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)

    def handleFailure(self, node):
        nodeEntity = FailureProtocolEntity.fromProtocolTreeNode(node)
        self.toUpper(nodeEntity)
        self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT, reason = "Authentication Failure"))

    def handleStreamError(self, node):
        nodeEntity = StreamErrorProtocolEntity.fromProtocolTreeNode(node)
        errorType = nodeEntity.getErrorType()

        if not errorType:
            raise NotImplementedError("Unhandled stream:error node:\n%s" % node)

        self.toUpper(nodeEntity)
