from yowsup.layers import YowLayer, YowLayerEvent
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
    EVENT_STATE_PING_OK         = "org.openwhatsapp.yowsup.event.network.pingok"
    EVENT_STATE_PING_KO         = "org.openwhatsapp.yowsup.event.network.pingko"

    PROP_ENDPOINT               = "org.openwhatsapp.yowsup.prop.endpoint"
    PROP_NET_READSIZE           = "org.openwhatsapp.yowsup.prop.net.readSize"

    def __init__(self):
        YowLayer.__init__(self)
        self.interface = YowNetworkLayerInterface(self)
        asyncore.dispatcher.__init__(self)
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

    def onEvent(self, ev):
        if ev.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            self.createConnection()
            return True
        elif ev.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECT:
            self.destroyConnection(ev.getArg("reason"))
            return True

    def createConnection(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_buffer = bytearray()
        endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
        logger.debug("Connecting to %s:%s" % endpoint)
        if self.proxyHandler != None:
            logger.debug("HttpProxy connect: %s:%d" % endpoint)
            self.proxyHandler.connect(self, endpoint)
        else:
            self.connect(endpoint)

    def destroyConnection(self, reason = None):
        self.handle_close(reason or "Requested")

    def getStatus(self):
        return self.connected

    def handle_connect(self):
        self.connected = True
        if self.proxyHandler != None:
            logger.debug("HttpProxy handle connect")
            self.proxyHandler.send(self)
        else:
            self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def handle_close(self, reason = "Connection Closed"):
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
