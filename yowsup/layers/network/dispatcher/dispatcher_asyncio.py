from yowsup.layers.network.dispatcher.dispatcher import YowConnectionDispatcher
import asyncio
import logging
import socket
import traceback

logger = logging.getLogger(__name__)

class AsyncioConnectionDispatcher(YowConnectionDispatcher):
    def __init__(self, connectionCallbacks):
        super().__init__(connectionCallbacks)
        self._connected = False
        self.loop = asyncio.get_event_loop()
        self.sock = None

    async def _send_data(self, data):
        if self._connected:
            self.sock.sendall(data)
        else:
            logger.warning("Attempted to send %d bytes while still not connected", len(data))

    def sendData(self, data):
        asyncio.run(self._send_data(data))

    async def _connect(self, host):
        logger.debug("connect(%s)", str(host))
        self.connectionCallbacks.onConnecting()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(False)
        try:
            await self.loop.sock_connect(self.sock, host)
            self._connected = True
            self.connectionCallbacks.onConnected()
        except Exception as e:
            logger.error("Connection failed: %s", str(e))
            self.connectionCallbacks.onDisconnected()

    def connect(self, host):
        self.loop.run_until_complete(self._connect(host))

    def handle_connect(self):
        logger.debug("handle_connect")
        if not self._connected:
            self._connected = True
            self.connectionCallbacks.onConnected()

    def handle_close(self):
        logger.debug("handle_close")
        if self._connected and self.sock:
            self.sock.close()
            self._connected = False
            self.connectionCallbacks.onDisconnected()

    def handle_error(self):
        logger.error(traceback.format_exc())
        self.handle_close()

    async def _handle_read(self):
        if self._connected:
            try:
                data = await self.loop.sock_recv(self.sock, 1024)
                self.connectionCallbacks.onRecvData(data)
            except Exception as e:
                logger.error("Read failed: %s", str(e))
                self.handle_close()

    def handle_read(self):
        asyncio.run(self._handle_read())

    def disconnect(self):
        logger.debug("disconnect")
        self.handle_close()
