from Yowsup.layers import YowLayer, YowLayerEvent
import asyncore, socket, threading, sys, traceback
from .networkerror import NetworkError
class YowNetworkLayer(YowLayer, asyncore.dispatcher_with_send):
    '''
        send:       bytearray -> None
        receive:    bytearray -> bytearray
    '''

    EVENT_STATE_CONNECT     = "network.state.connect"
    EVENT_STATE_DISCONNECT  = "network.state.disconnect"
    EVENT_STATE_CONNECTED   = "network.state.connected"

    def __init__(self):
        YowLayer.__init__(self)
        asyncore.dispatcher.__init__(self)
        
    def onEvent(self, ev):
        if ev.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
            self.out_buffer = bytearray()
            self.connect(self.__class__.getProp("endpoint"))
            return True

    def handle_connect(self):
        self.emitEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECTED))

    def handle_close(self):
        self.close()
        raise NetworkError("Connection Closed")

    def handle_error(self):
        raise

    def handle_read(self):
        readSize = self.__class__.getProp("readSize", 1024)
        data = self.recv(readSize)
        self.receive(data)

    def send(self, data):
        self.out_buffer = self.out_buffer + data

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Network Layer"
