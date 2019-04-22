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

        self.stack = stackBuilder \
            .pushDefaultLayers() \
            .push(SyncLayer) \
            .build()

        self.stack.setProp(SyncLayer.PROP_CONTACTS, contacts)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        self.stack.loop()
