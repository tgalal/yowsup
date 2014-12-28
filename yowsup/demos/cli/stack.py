from yowsup.stacks import YowStack, YOWSUP_CORE_LAYERS, YOWSUP_PROTOCOL_LAYERS_FULL
from yowsup.layers.axolotl import YowAxolotlLayer
from .layer import YowsupCliLayer
from yowsup.common import YowConstants
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.auth import AuthError
from yowsup.layers.coder import YowCoderLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup import env
from yowsup.env import S40YowsupEnv
import sys

class YowsupCliStack(object):
    def __init__(self, credentials, encryptionEnabled = False):
        if encryptionEnabled:
            stackStruct = \
                (YowsupCliLayer,) +\
                (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                (YowAxolotlLayer,) +\
                YOWSUP_CORE_LAYERS

        else:
            env.CURRENT_ENV = S40YowsupEnv()
            stackStruct = \
                (YowsupCliLayer,) +\
                (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                YOWSUP_CORE_LAYERS

        self.stack = YowStack(stackStruct)

        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)

    def start(self):
        print("Yowsup Cli client\n==================\nType /help for available commands\n")
        self.stack.broadcastEvent(YowLayerEvent(YowsupCliLayer.EVENT_START))

        try:
            self.stack.loop(timeout = 0.5, discrete = 0.5)
        except AuthError as e:
            print("Auth Error, reason %s" % e)
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
