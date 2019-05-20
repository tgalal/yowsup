from yowsup.stacks import  YowStackBuilder
from .layer import MediaSinkLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer


class MediaSinkStack(object):
    def __init__(self, profile, storage_dir=None):
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(MediaSinkLayer)\
            .build()
        self._stack.setProp(MediaSinkLayer.PROP_STORAGE_DIR, storage_dir)
        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()
