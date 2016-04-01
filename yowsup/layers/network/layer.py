from yowsup.layers import YowLayer, YowLayerEvent, EventCallback
from yowsup.common.http.httpproxy import HttpProxy
from yowsup.layers.network.layer_interface import YowNetworkLayerInterface
import asyncore, socket, logging
logger = logging.getLogger(__name__)

class YowNetworkLayer(YowLayer, asyncore.dispatcher_with_send):
    '''
        send:       bytearray -> None
        receive:    bytearray -> bytearray
    '''

    EVENT_STATE_CONNECT         = "org.openwhatsapp.yowsup.event.network.connect"
    EVENT_STATE_DISCONNECT      = "org.openwhatsapp.yowsup.event.network.disconnect"
    EVENT_STATE_CONNECTED       = "org.openwhatsapp.yowsup.event.network.connected"
    EVENT_STATE_DISCONNECTED    = "org.openwhatsapp.yowsup.event.network.disconnected"

    PROP_ENDPOINT               = "org.openwhatsapp.yowsup.prop.endpoint"
    PROP_NET_READSIZE           = "org.openwhatsapp.yowsup.prop.net.readSize"

    STATE_DISCONNECTED          = 0
    STATE_CONNECTING            = 1
    STATE_CONNECTED             = 2
    STATE_DISCONNECTING         = 3

    def __init__(self):
        asyncore.dispatcher.__init__(self)
        self.state = self.__class__.STATE_DISCONNECTED
        YowLayer.__init__(self)
        self.interface = YowNetworkLayerInterface(self)
        httpProxy = HttpProxy.getFromEnviron()
        proxyHandler = None
        if httpProxy != None:
            logger.debug("HttpProxy initialize: %s" % httpProxy)
            def onConnect():
                logger.debug("HttpProxy connected")
                self.proxyHandler = None
                self.handle_connect()
            proxyHandler = httpProxy.handler()
            proxyHandler.onConnect = onConnect
        self.proxyHandler = proxyHandler

    @EventCallback(EVENT_STATE_CONNECT)
    def onConnect(self, ev):
        self.createConnection()
        return True

    @EventCallback(EVENT_STATE_DISCONNECT)
    def onDisconnect(self, ev):
        self.destroyConnection(ev.getArg("reason"))
        return True

    def createConnection(self):
        self.state = self.__class__.STATE_CONNECTING
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_buffer = bytearray()
        endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
        logger.debug("Connecting to %s:%s" % endpoint)
        if self.proxyHandler != None:
            logger.debug("HttpProxy connect: %s:%d" % endpoint)
            self.proxyHandler.connect(self, endpoint)
        else:
            try:
                self.connect(endpoint)
            except OSError as e:
                self.handle_close(e)

    def destroyConnection(self, reason = None):
        self.state = self.__class__.STATE_DISCONNECTING
        self.handle_close(reason or "Requested")

    def getStatus(self):
        return self.connected

    def handle_connect(self):
        self.state = self.__class__.STATE_CONNECTED
        self.connected = True
        if self.proxyHandler != None:
            logger.debug("HttpProxy handle connect")
            self.proxyHandler.send(self)
        else:
            self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def handle_close(self, reason = "Connection Closed"):
        if self.state != self.__class__.STATE_DISCONNECTED:
            self.state = self.__class__.STATE_DISCONNECTED
            self.connected = False
            logger.debug("Disconnected, reason: %s" % reason)
            self.emitEvent(YowLayerEvent(self.__class__.EVENT_STATE_DISCONNECTED, reason = reason, detached=True))
            self.close()

    def handle_error(self):
        raise

    def handle_read(self):
        readSize = self.getProp(self.__class__.PROP_NET_READSIZE, 1024)
        if self.proxyHandler != None:
            data = self.proxyHandler.recv(self, readSize)
            logger.debug("HttpProxy handle read: %s" % data)
        else:
            data = self.recv(readSize)
            self.receive(data)

    def send(self, data):
        if self.connected:
            self.out_buffer = self.out_buffer + data
            self.initiate_send()

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Network Layer"
