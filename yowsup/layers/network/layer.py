from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.common.http.httpproxy import HttpProxy
from twisted.python import log
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory, Protocol

import sys
import logging
logger = logging.getLogger(__name__)

class YowNetworkLayer(YowLayer):
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

    def __init__(self):
        YowLayer.__init__(self)

    def onEvent(self, ev):
        if ev.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            logger.debug("Got connect event")
            endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
            self.ynpf = YowNetworkProtocolFactory(self)
            log.startLogging(sys.stdout)
            reactor.connectTCP(endpoint[0], endpoint[1], self.ynpf)
            logger.debug("connected!")
            return True
        elif ev.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECT:
            self.handle_close(ev.getArg("reason") or "Requested")
            return True

    def __str__(self):
        return "Network Layer"

    def send(self, data):
        self.ynpf.connectedProtocol.send(data)

    def receive(self, data):
        self.toUpper(data)


class YowNetworkProtocol(Protocol):
    def __init__(self, network_layer):
        self.network_layer = network_layer

    def dataReceived(self, data):
        self.network_layer.toUpper(data)

    def send(self, data):
        logger.debug("writin %s" % data)
        self.transport.write(str(data))
        logger.debug("done writin %s" % data)

    def connectionMade(self):
        logger.debug("connectionMade")
        self.network_layer.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))


class YowNetworkProtocolFactory(ClientFactory):
    def __init__(self, network_layer):
        self.network_layer = network_layer

    def startedConnecting(self,connector):
        logger.debug("Connecting")

    def clientConnectionLost(self, connector, reason = "Connection Closed"):
        logger.debug("Disconnected, reason: %s" % reason)
        self.network_layer.emitEvent(YowLayerEvent(self.network_layer.__class__.EVENT_STATE_DISCONNECTED, reason = reason, detached=True))

    def clientConnectionFailed(self, connector, reason):
        logger.debug("Connection Failed, reason: %s" % reason)
        self.network_layer.emitEvent(YowLayerEvent(self.network_layer.__class__.EVENT_STATE_DISCONNECTED, reason = reason, detached=True))

    def buildProtocol(self, addr):
        logger.debug("Connected, Building protocol")
        self.connectedProtocol = YowNetworkProtocol(self.network_layer)
        self.connectedProtocol.factory = self
        return self.connectedProtocol
