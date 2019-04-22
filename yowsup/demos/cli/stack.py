from yowsup.stacks import  YowStackBuilder
from .layer import YowsupCliLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
import sys


class YowsupCliStack(object):
    def __init__(self, credentials):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers()\
            .push(YowsupCliLayer)\
            .build()

        # self.stack.setCredentials(credentials)
        self.stack.setCredentials(credentials)
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        print("Yowsup Cli client\n==================\nType /help for available commands\n")
        self.stack.broadcastEvent(YowLayerEvent(YowsupCliLayer.EVENT_START))

        try:
            self.stack.loop()
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
