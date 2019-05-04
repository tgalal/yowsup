from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers import EventCallback
import sys

try:
    from tqdm import tqdm
    import requests
except ImportError:
    print("This demo requires the python packages 'tqdm' and 'requests' to be installed, exiting.")
    sys.exit(1)

from ..common.sink_worker import SinkWorker

import tempfile
import logging
import os

logger = logging.getLogger(__name__)


class MediaSinkLayer(YowInterfaceLayer):
    PROP_STORAGE_DIR = "org.openwhatsapp.yowsup.prop.demos.mediasink.storage_dir"

    def __init__(self):
        super(MediaSinkLayer, self).__init__()
        self._sink_worker = None

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def on_connected(self, event):
        logger.info("Connected, starting SinkWorker")
        storage_dir = self.getProp(self.PROP_STORAGE_DIR)
        if storage_dir is None:
            logger.debug("No storage dir specified, creating tempdir")
            storage_dir = tempfile.mkdtemp("yowsup_mediasink")

        if not os.path.exists(storage_dir):
            logger.debug("%s does not exist, creating" % storage_dir)
            os.makedirs(storage_dir)

        logger.info("Storing incoming media to %s" % storage_dir)
        self._sink_worker = SinkWorker(storage_dir)
        self._sink_worker.start()

    @ProtocolEntityCallback("message")
    def on_message(self, message_protocolentity):
        self.toLower(message_protocolentity.ack())
        self.toLower(message_protocolentity.ack(True))
        if isinstance(message_protocolentity, MediaMessageProtocolEntity):
            self.on_media_message(message_protocolentity)

    @ProtocolEntityCallback("receipt")
    def on_receipt(self, entity):
        self.toLower(entity.ack())

    def on_media_message(self, media_message_protocolentity):
        self._sink_worker.enqueue(media_message_protocolentity)

