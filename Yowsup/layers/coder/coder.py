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
        self.reader = Reader(self)
        self.readBuf = bytearray()
        self.readStreamStarted = False

    def onEvent(self, event):
        if event.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            self.writer.streamStart(
                self.getProp(self.__class__.PROP_DOMAIN),
                self.getProp(self.__class__.PROP_RESOURCE)
            )
            self.readStreamStarted = False
            return

    def send(self, data):
        self.writer.write(data)

    def receive(self, data):
        self.readBuf = self.readBuf + data
        if not self.readStreamStarted:
            self.readStreamStarted = True
            self.reader.streamStart()
            #self.toUpper(self.reader.nextTree())
        else:
            self.toUpper(self.reader.nextTree())

    def write(self, i):
        if(type(i) in(list, tuple)):
            self.toLower(bytearray(i))
        else:
            self.toLower(bytearray([i]))


    def readAll(self):
        result = self.readBuf
        self.readBuf = bytearray()
        return result

    def read(self, _ = None):
        return self.readBuf.pop(0)

    def __str__(self):
        return "Coder Layer"