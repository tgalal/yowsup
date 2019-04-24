from yowsup.layers.network.dispatcher.dispatcher import YowConnectionDispatcher
import socket
import logging

logger = logging.getLogger(__name__)


class SocketConnectionDispatcher(YowConnectionDispatcher):
    def __init__(self, connectionCallbacks):
        super(SocketConnectionDispatcher, self).__init__(connectionCallbacks)
        self.socket = None

    def connect(self, host):
        if not self.socket:
            self.socket = socket.socket()
            self.connectAndLoop(host)
        else:
            logger.error("Already connected?")

    def disconnect(self):
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_WR)
                self.socket.close()
            except socket.error as e:
                logger.error(e)
                self.socket = None
                self.connectionCallbacks.onDisconnected()
        else:
            logger.error("Not connected?")

    def connectAndLoop(self, host):
        socket = self.socket
        self.connectionCallbacks.onConnecting()
        try:
            socket.connect(host)
            self.connectionCallbacks.onConnected()
            while True:
                data = socket.recv(1024)
                if len(data):
                    self.connectionCallbacks.onRecvData(data)
                else:
                    break
            self.connectionCallbacks.onDisconnected()
        except Exception as e:
            logger.error(e)
            self.connectionCallbacks.onConnectionError(e)
        finally:
            self.socket = None
            socket.close()

    def sendData(self, data):
        try:
            self.socket.send(data)
        except socket.error as e:
            logger.error(e)
            self.disconnect()
