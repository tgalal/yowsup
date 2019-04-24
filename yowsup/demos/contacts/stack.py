from .layer import SyncLayer

from yowsup.stacks import  YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.network import YowNetworkLayer


class YowsupSyncStack(object):
    def __init__(self, credentials, contacts):
        """
        :param credentials:
        :param contacts: list of [jid ]
        :return:
        """
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder \
            .pushDefaultLayers() \
            .push(SyncLayer) \
            .build()

        self._stack.setProp(SyncLayer.PROP_CONTACTS, contacts)
        self._stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self._stack.setCredentials(credentials)

    def set_prop(self, key, val):
        self._stack.setProp(key, val)

    def start(self):
        self._stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self._stack.loop()
