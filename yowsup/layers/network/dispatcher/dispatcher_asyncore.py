from yowsup.layers.network.dispatcher.dispatcher import YowConnectionDispatcher
import asyncore
import logging
import threading
import socket

logger = logging.getLogger(__name__)

'''
    WIP, not finished and 
    doesn't seem to be working properly, need to check why
'''

class AsyncoreConnectionDispatcher(YowConnectionDispatcher, asyncore.dispatcher_with_send):
    def __init__(self, connectionCallbacks):
        super(AsyncoreConnectionDispatcher, self).__init__(connectionCallbacks)
        asyncore.dispatcher_with_send.__init__(self)

    def sendData(self, data):
        if self.connected:
            self.out_buffer = self.out_buffer + data
            self.initiate_send()

    def connect(self, host):
        threading.Thread(target=self.__loop, args=(host,)).start()

    def handle_connect(self):
        if not self.connected:
            self.connectionCallbacks.onConnected()

    def handle_close(self):
        self.connectionCallbacks.onDisonnected()

    def handle_read(self):
        data = self.recv(1024)
        self.connectionCallbacks.onRecvData(data)

    def handle_error(self):
        pass

    def __loop(self, host):
        self.connectionCallbacks.onConnecting()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        asyncore.dispatcher_with_send.connect(self, host)
        logger.debug("Entering loop")
        asyncore.loop()
        logger.debug("Exited loop")

    def disconnect(self):
        self.close()
