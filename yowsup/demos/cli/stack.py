from yowsup.stacks import  YowStackBuilder
from .layer import YowsupCliLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
import sys


class YowsupCliStack(object):
    def __init__(self, credentials):
        stackBuilder = YowStackBuilder()

        self._stack = stackBuilder\
            .pushDefaultLayers()\
            .push(YowsupCliLayer)\
            .build()

        self._stack.setCredentials(credentials)
        self._stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def set_prop(self, prop, val):
        self._stack.setProp(prop, val)

    def start(self):
        print("Yowsup Cli client\n==================\nType /help for available commands\n")
        self._stack.broadcastEvent(YowLayerEvent(YowsupCliLayer.EVENT_START))

        try:
            self._stack.loop()
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)
