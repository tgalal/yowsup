from consonance.protocol import WANoiseProtocol
from consonance.streams.segmented.segmented import SegmentedStream
from consonance.config.client import ClientConfig
from dissononce.dh.keypair import KeyPair
from dissononce.dh.x25519.x25519 import PublicKey

import threading


class WANoiseProtocolHandshakeWorker(threading.Thread):
    def __init__(self, wanoiseprotocol, stream, client_config, s, rs=None, finish_callback=None):
        """
        :param wanoiseprotocol:
        :type wanoiseprotocol: WANoiseProtocol
        :param stream:
        :type stream: SegmentedStream
        :param client_config:
        :type client_config: ClientConfig
        :param s:
        :type s: KeyPair
        :param rs:
        :type rs: PublicKey | None
        """
        super(WANoiseProtocolHandshakeWorker, self).__init__()
        self.daemon = True

        self._protocol = wanoiseprotocol # type: WANoiseProtocol
        self._stream = stream # type: SegmentedStream
        self._client_config = client_config # type: ClientConfig
        self._s = s # type: KeyPair
        self._rs = rs # type: PublicKey
        self._finish_callback = finish_callback

    def run(self):
        self._protocol.reset()
        self._protocol.start(self._stream, self._client_config, self._s, self._rs)
        if self._finish_callback is not None:
            self._finish_callback()
