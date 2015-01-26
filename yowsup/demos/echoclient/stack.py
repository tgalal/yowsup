from .layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.network                     import YowNetworkLayer
from yowsup import env
from yowsup.stacks import YowStackBuilder
class YowsupEchoStack(object):
    def __init__(self, credentials, encryptionEnabled = False):

        if not encryptionEnabled:
            env.CURRENT_ENV = env.S40YowsupEnv()

        self.stack = YowStackBuilder.getDefaultStack(EchoLayer, encryptionEnabled, groups=False, media = True, privacy=False)
        self.stack.setCredentials(credentials)

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
