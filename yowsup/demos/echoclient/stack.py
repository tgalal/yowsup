from yowsup.stacks import  YowStackBuilder
from .layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer


class YowsupEchoStack(object):
    def __init__(self, credentials):
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(EchoLayer)\
            .build()

        self._stack.setCredentials(credentials)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()
