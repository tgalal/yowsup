from Yowsup.layers import YowLayer
import asyncore, socket, threading, sys, traceback
from networkerror import NetworkError
class YowNetworkLayer(YowLayer, asyncore.dispatcher_with_send):

    def __init__(self):
        YowLayer.__init__(self)
        asyncore.dispatcher.__init__(self)
        
    def init(self):
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.out_buffer = ""
        self.connect(self.__class__.getProp("endpoint"))
        return True

    def handle_connect(self):
        self.initUpper()

    def handle_close(self):
        self.close()
        raise NetworkError("Connection Closed")

    def handle_error(self):
        exception, value, _traceback = sys.exc_info()
        print traceback.format_tb(_traceback)
        raise exception(value)

    def handle_read(self):
        readSize = self.__class__.getProp("readSize", 1024)
        data = self.recv(readSize)
        self.receive([ord(i) for i in data])

    def send(self, data):
        self.out_buffer = self.out_buffer  + "".join([chr(d) for d in data])

    def receive(self, data):
        self.toUpper(data)
