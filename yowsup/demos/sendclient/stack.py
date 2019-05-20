from yowsup.stacks import  YowStackBuilder
from .layer import SendLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.network import YowNetworkLayer


class YowsupSendStack(object):
    def __init__(self, profile, messages):
        """
        :param profile:
        :param messages: list of (jid, message) tuples
        :return:
        """
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(SendLayer)\
            .build()

        self._stack.setProp(SendLayer.PROP_MESSAGES, messages)
        self._stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self._stack.setProfile(profile)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()
