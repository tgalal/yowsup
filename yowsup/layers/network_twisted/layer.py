from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.internet.endpoints import TCP4ClientEndpoint, connectProtocol
import socket, logging
logger = logging.getLogger(__name__)

class YowTwistedNetworkLayer(YowLayer, Protocol):

    def __init__(self):
        YowLayer.__init__(self)
        
    def onEvent(self, ev):
        if ev.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            #self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            #self.out_buffer = bytearray()
            endpoint = self.getProp(YowNetworkLayer.PROP_ENDPOINT)
            point = TCP4ClientEndpoint(reactor, endpoint[0], endpoint[1])
            connectProtocol(point, self)
            #self.connect(endpoint)
            return True
        elif ev.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECT:
            self.handle_close(ev.getArg("reason") or "Requested")
            return True

    #def handle_connect(self):
    def connectionMade(self):
        print "conenction made"
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def handle_close(self, reason = "Connection Closed"):
        logger.debug("Disconnect, reason: %s" % reason)
        self.transport.loseConnection()
        self.connectionLost(self, reason)

    def connectionLost(self, reason):
        logger.debug("Disconnected, reason: %s" % reason)
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECTED, reason = reason, detached=True))
        #self.close()
        
    #def handle_error(self):
    #    raise

    #def handle_read(self):
    def dataReceived(self, data):
        self.receive(data)

    def send(self, data):
        self.transport.write( bytes( data ) )
        #self.out_buffer = self.out_buffer + data
        #self.initiate_send()

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Twisted Network Layer"
