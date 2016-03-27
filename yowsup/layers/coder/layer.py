from yowsup.layers import YowLayer, YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
from .encoder import WriteEncoder
from .decoder import ReadDecoder
from .tokendictionary import TokenDictionary
class YowCoderLayer(YowLayer):

    PROP_DOMAIN =   "org.openwhatsapp.yowsup.prop.domain"
    PROP_RESOURCE = "org.openwhatsapp.yowsup.prop.resource"

    def __init__(self):
        YowLayer.__init__(self)
        tokenDictionary = TokenDictionary()
        self.writer = WriteEncoder(tokenDictionary)
        self.reader = ReadDecoder(tokenDictionary)
    
    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, event):
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