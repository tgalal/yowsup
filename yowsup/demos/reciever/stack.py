from yowsup.stacks import  YowStackBuilder
from .layer import RecieverLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer


class YowsupRecieverStack(object):
    def __init__(self, profile):
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(RecieverLayer)\
            .build()

        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()
