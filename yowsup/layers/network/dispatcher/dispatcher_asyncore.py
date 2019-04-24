from yowsup.layers.network.dispatcher.dispatcher import YowConnectionDispatcher
import asyncore
import logging
import socket
import traceback

logger = logging.getLogger(__name__)


class AsyncoreConnectionDispatcher(YowConnectionDispatcher, asyncore.dispatcher_with_send):
    def __init__(self, connectionCallbacks):
        super(AsyncoreConnectionDispatcher, self).__init__(connectionCallbacks)
        asyncore.dispatcher_with_send.__init__(self)
        self._connected = False

    def sendData(self, data):
        if self._connected:
            self.out_buffer = self.out_buffer + data
            self.initiate_send()
        else:
            logger.warn("Attempted to send %d bytes while still not connected" % len(data))

    def connect(self, host):
        logger.debug("connect(%s)" % str(host))
        self.connectionCallbacks.onConnecting()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        asyncore.dispatcher_with_send.connect(self, host)
        asyncore.loop(timeout=1)

    def handle_connect(self):
        logger.debug("handle_connect")
        if not self._connected:
            self._connected = True
            self.connectionCallbacks.onConnected()

    def handle_close(self):
        logger.debug("handle_close")
        self.close()
        self._connected = False
        self.connectionCallbacks.onDisconnected()

    def handle_error(self):
        logger.error(traceback.format_exc())
        self.handle_close()

    def handle_read(self):
        data = self.recv(1024)
        self.connectionCallbacks.onRecvData(data)

    def disconnect(self):
        logger.debug("disconnect")
        self.handle_close()
