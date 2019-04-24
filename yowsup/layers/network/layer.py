from yowsup.layers import YowLayer, YowLayerEvent, EventCallback
from yowsup.layers.network.layer_interface import YowNetworkLayerInterface
from yowsup.layers.network.dispatcher.dispatcher import ConnectionCallbacks
from yowsup.layers.network.dispatcher.dispatcher import YowConnectionDispatcher
from yowsup.layers.network.dispatcher.dispatcher_socket import SocketConnectionDispatcher
from yowsup.layers.network.dispatcher.dispatcher_asyncore import AsyncoreConnectionDispatcher
import logging
logger = logging.getLogger(__name__)


class YowNetworkLayer(YowLayer, ConnectionCallbacks):
    """This layer wraps a connection dispatcher that provides connection and a communication channel
    to remote endpoints. Unless explicitly configured, applications should not make assumption about
    the dispatcher being used as the default dispatcher could be changed across versions"""
    EVENT_STATE_CONNECT         = "org.openwhatsapp.yowsup.event.network.connect"
    EVENT_STATE_DISCONNECT      = "org.openwhatsapp.yowsup.event.network.disconnect"
    EVENT_STATE_CONNECTED       = "org.openwhatsapp.yowsup.event.network.connected"
    EVENT_STATE_DISCONNECTED    = "org.openwhatsapp.yowsup.event.network.disconnected"

    PROP_ENDPOINT               = "org.openwhatsapp.yowsup.prop.endpoint"
    PROP_NET_READSIZE           = "org.openwhatsapp.yowsup.prop.net.readSize"
    PROP_DISPATCHER             = "org.openwhatsapp.yowsup.prop.net.dispatcher"

    STATE_DISCONNECTED          = 0
    STATE_CONNECTING            = 1
    STATE_CONNECTED             = 2
    STATE_DISCONNECTING         = 3

    DISPATCHER_SOCKET = 0
    DISPATCHER_ASYNCORE = 1
    DISPATCHER_DEFAULT = DISPATCHER_SOCKET

    def __init__(self):
        self.state = self.__class__.STATE_DISCONNECTED
        YowLayer.__init__(self)
        ConnectionCallbacks.__init__(self)
        self.interface = YowNetworkLayerInterface(self)
        self.connected = False
        self._dispatcher = None  # type: YowConnectionDispatcher

    def __create_dispatcher(self, dispatcher_type):
        if dispatcher_type == self.DISPATCHER_ASYNCORE:
            logger.debug("Created asyncore dispatcher")
            return AsyncoreConnectionDispatcher(self)
        else:
            logger.debug("Created socket dispatcher")
            return SocketConnectionDispatcher(self)

    def onConnected(self):
        logger.debug("Connected")
        self.state = self.__class__.STATE_CONNECTED
        self.connected = True
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def onDisconnected(self):
        if self.state != self.__class__.STATE_DISCONNECTED:
            self.state = self.__class__.STATE_DISCONNECTED
            self.connected = False
            logger.debug("Disconnected")
            self.emitEvent(YowLayerEvent(self.__class__.EVENT_STATE_DISCONNECTED, reason="", detached=True))

    def onConnecting(self):
        pass

    def onConnectionError(self, error):
        self.onDisconnected()

    @EventCallback(EVENT_STATE_CONNECT)
    def onConnectLayerEvent(self, ev):
        if not self.connected:
            self.createConnection()
        else:
            logger.warn("Received connect event while already connected")
        return True

    @EventCallback(EVENT_STATE_DISCONNECT)
    def onDisconnectLayerEvent(self, ev):
        self.destroyConnection(ev.getArg("reason"))
        return True

    def createConnection(self):
        self._dispatcher = self.__create_dispatcher(self.getProp(self.PROP_DISPATCHER, self.DISPATCHER_DEFAULT))
        self.state = self.__class__.STATE_CONNECTING
        endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
        logger.info("Connecting to %s:%s" % endpoint)
        self._dispatcher.connect(endpoint)

    def destroyConnection(self, reason = None):
        self.state = self.__class__.STATE_DISCONNECTING
        self._dispatcher.disconnect()

    def getStatus(self):
        return self.connected

    def send(self, data):
        if self.connected:
            self._dispatcher.sendData(data)

    def onRecvData(self, data):
        self.receive(data)

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Network Layer"
