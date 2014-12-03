from yowsup.layers import YowLayer, YowLayerEvent
import asyncore, socket
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

    def __init__(self):
        YowLayer.__init__(self)
        asyncore.dispatcher.__init__(self)
        
    def onEvent(self, ev):
        if ev.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.out_buffer = bytearray()
            self.connect(self.getProp(self.__class__.PROP_ENDPOINT))
            return True
        elif ev.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECT:
            self.handle_close(ev.getArg("reason") or "Requested")
            return True

    def handle_connect(self):
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def handle_close(self, reason = "Connection Closed"):
        print("Disconnected, reason: %s" % reason)
        self.emitEvent(YowLayerEvent(self.__class__.EVENT_STATE_DISCONNECTED, reason = reason))
        self.close()
        #raise NetworkError("Connection Closed")

    def handle_error(self):
        raise

    def handle_read(self):
        readSize = self.getProp(self.__class__.PROP_NET_READSIZE, 1024)
        data = self.recv(readSize)
        self.receive(data)

    def send(self, data):
        self.out_buffer = self.out_buffer + data
        self.initiate_send()

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Network Layer"
