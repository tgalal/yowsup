from Yowsup.layers import YowLayer, YowLayerEvent
from Yowsup.layers.network import YowNetworkLayer
from .writer import Writer
from .reader import Reader
class YowCoderLayer(YowLayer):

    PROP_DOMAIN =   "org.openwhatsapp.yowsup.prop.domain"
    PROP_RESOURCE = "org.openwhatsapp.yowsup.prop.resource"

    def __init__(self):
        YowLayer.__init__(self)
        self.writer = Writer(self)
        self.reader = Reader()

    def onEvent(self, event):
        if event.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            self.writer.streamStart(
                self.getProp(self.__class__.PROP_DOMAIN),
                self.getProp(self.__class__.PROP_RESOURCE)
            )
            self.reader.reset()

    def send(self, data):
        self.writer.write(data)

    def receive(self, data):
        node = self.reader.getProtocolTreeNode(data)
        if node:
            self.toUpper(node)

    def write(self, i):
        if(type(i) in(list, tuple)):
            self.toLower(bytearray(i))
        else:
            self.toLower(bytearray([i]))

    def __str__(self):
        return "Coder Layer"