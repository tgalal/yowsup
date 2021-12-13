from yowsup.layers.noise.workers.handshake import WANoiseProtocolHandshakeWorker
from yowsup.layers import YowLayer, EventCallback
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers.noise.layer_noise_segments import YowNoiseSegmentsLayer
from yowsup.config.manager import ConfigManager
from yowsup.env.env import YowsupEnv
from yowsup.layers import YowLayerEvent
from yowsup.structs.protocoltreenode import ProtocolTreeNode
from yowsup.layers.coder.encoder import WriteEncoder
from yowsup.layers.coder.tokendictionary import TokenDictionary

from consonance.protocol import WANoiseProtocol
from consonance.config.client import ClientConfig
from consonance.config.useragent import UserAgentConfig
from consonance.streams.segmented.blockingqueue import BlockingQueueSegmentedStream
from consonance.structs.keypair import KeyPair

import threading
import logging


logger = logging.getLogger(__name__)
try:
    import Queue
except ImportError:
    import queue as Queue


class YowNoiseLayer(YowLayer):
    DEFAULT_PUSHNAME = "yowsup"
    HEADER = b'WA\x03\x00'
    EDGE_HEADER = b'ED\x00\x01'
    EVENT_HANDSHAKE_FAILED = "org.whatsapp.yowsup.layer.noise.event.handshake_failed"

    def __init__(self):
        super(YowNoiseLayer, self).__init__()
        self._wa_noiseprotocol = WANoiseProtocol(
            3, 0, protocol_state_callbacks=self._on_protocol_state_changed
        )  # type: WANoiseProtocol

        self._handshake_worker = None
        self._stream = BlockingQueueSegmentedStream()  # type: BlockingQueueSegmentedStream
        self._read_buffer = bytearray()
        self._flush_lock = threading.Lock()
        self._incoming_segments_queue = Queue.Queue()
        self._profile = None
        self._rs = None

    def __str__(self):
        return "Noise Layer"

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def on_disconnected(self, event):
        self._wa_noiseprotocol.reset()

    @EventCallback(YowAuthenticationProtocolLayer.EVENT_AUTH)
    def on_auth(self, event):
        logger.debug("Received auth event")
        self._profile = self.getProp("profile")
        config = self._profile.config  # type: yowsup.config.v1.config.Config
        # event's keypair will override config's keypair
        local_static = config.client_static_keypair
        username = int(self._profile.username)

        if local_static is None:
            logger.error("client_static_keypair is not defined in specified config, disconnecting")
            self.broadcastEvent(
                YowLayerEvent(
                    YowNetworkLayer.EVENT_STATE_DISCONNECT,
                    reason="client_static_keypair is not defined in specified config"
                )
            )
        else:
            if type(local_static) is bytes:
                local_static = KeyPair.from_bytes(local_static)
            assert type(local_static) is KeyPair, type(local_static)
            passive = event.getArg('passive')

            self.setProp(YowNoiseSegmentsLayer.PROP_ENABLED, False)

            if config.edge_routing_info:
                self.toLower(self.EDGE_HEADER)
                self.setProp(YowNoiseSegmentsLayer.PROP_ENABLED, True)
                self.toLower(config.edge_routing_info)
                self.setProp(YowNoiseSegmentsLayer.PROP_ENABLED, False)

            self.toLower(self.HEADER)
            self.setProp(YowNoiseSegmentsLayer.PROP_ENABLED, True)

            remote_static = config.server_static_public

            self._rs = remote_static
            yowsupenv = YowsupEnv.getCurrent()
            client_config = ClientConfig(
                username=username,
                passive=passive,
                useragent=UserAgentConfig(
                    platform=0,
                    app_version=yowsupenv.getVersion(),
                    mcc=config.mcc or "000",
                    mnc=config.mnc or "000",
                    os_version=yowsupenv.getOSVersion(),
                    manufacturer=yowsupenv.getManufacturer(),
                    device=yowsupenv.getDeviceName(),
                    os_build_number=yowsupenv.getOSVersion(),
                    phone_id=config.fdid or "",
                    locale_lang="en",
                    locale_country="US"
                ),
                pushname=config.pushname or self.DEFAULT_PUSHNAME,
                short_connect=True
            )
            if not self._in_handshake():
                logger.debug("Performing handshake [username= %d, passive=%s]" % (username, passive) )
                self._handshake_worker = WANoiseProtocolHandshakeWorker(
                    self._wa_noiseprotocol, self._stream, client_config, local_static, remote_static,
                    self.on_handshake_finished
                )
                logger.debug("Starting handshake worker")
                self._stream.set_events_callback(self._handle_stream_event)
                self._handshake_worker.start()

    def on_handshake_finished(self, e=None):
        # type: (Exception) -> None
        if e is not None:
            self.emitEvent(YowLayerEvent(self.EVENT_HANDSHAKE_FAILED, reason=e))
            data=WriteEncoder(TokenDictionary()).protocolTreeNodeToBytes(
                ProtocolTreeNode("failure", {"reason": str(e)})
            )
            self.toUpper(data)
            logger.error("An error occurred during handshake, try login again.")

    def _in_handshake(self):
        """
        :return:
        :rtype: bool
        """
        return self._wa_noiseprotocol.state == WANoiseProtocol.STATE_HANDSHAKE

    def _on_protocol_state_changed(self, state):
        if state == WANoiseProtocol.STATE_TRANSPORT:
            if self._rs != self._wa_noiseprotocol.rs:
                config = self._profile.config
                config.server_static_public = self._wa_noiseprotocol.rs
                self._profile.write_config(config)
                self._rs = self._wa_noiseprotocol.rs
            self._flush_incoming_buffer()

    def _handle_stream_event(self, event):
        if event == BlockingQueueSegmentedStream.EVENT_WRITE:
            self.toLower(self._stream.get_write_segment())
        elif event == BlockingQueueSegmentedStream.EVENT_READ:
            self._stream.put_read_segment(self._incoming_segments_queue.get(block=True))

    def send(self, data):
        """
        :param data:
        :type data: bytearray | bytes
        :return:
        :rtype:
        """
        data = bytes(data) if type(data) is not bytes else data
        self._wa_noiseprotocol.send(data)

    def _flush_incoming_buffer(self):
        self._flush_lock.acquire()
        while self._incoming_segments_queue.qsize():
            self.toUpper(self._wa_noiseprotocol.receive())
        self._flush_lock.release()

    def receive(self, data):
        """
        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        self._incoming_segments_queue.put(data)
        if not self._in_handshake():
            self._flush_incoming_buffer()
