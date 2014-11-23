from Yowsup.layers import YowLayer, YowLayerEvent
from Yowsup.layers.network import YowNetworkLayer
from .writer import Writer
from .reader import Reader
class YowCoderLayer(YowLayer):

    PROP_DOMAIN =   "org.openwhatsapp.yowsup.prop.domain"
    PROP_RESOURCE = "org.openwhatsapp.yowsup.prop.resource"

    def __init__(self):
        YowLayer.__init__(self)
        self.writer = Writer()
        self.reader = Reader()

    def onEvent(self, event):
        if event.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            self.writer.reset()
            self.reader.reset()
            streamStartBytes = self.writer.getStreamStartBytes(
                self.getProp(self.__class__.PROP_DOMAIN),
                self.getProp(self.__class__.PROP_RESOURCE)
            )
            for i in range(0, 4):
                self.write(streamStartBytes.pop(0))
            self.write(streamStartBytes)

    def send(self, data):
        self.write(self.writer.protocolTreeNodeToBytes(data))

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