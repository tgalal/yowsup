from yowsup.stacks import  YowStackBuilder
from .layer import SendLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.network import YowNetworkLayer


class YowsupSendStack(object):
    def __init__(self, credentials, messages, encryptionEnabled = True):
        """
        :param credentials:
        :param messages: list of (jid, message) tuples
        :param encryptionEnabled:
        :return:
        """
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(SendLayer)\
            .build()

        self.stack.setProp(SendLayer.PROP_MESSAGES, messages)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
