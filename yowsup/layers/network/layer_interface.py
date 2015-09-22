from yowsup.layers import YowLayerInterface
class YowNetworkLayerInterface(YowLayerInterface):
    def connect(self):
        self._layer.createConnection()

    def disconnect(self):
        self._layer.destroyConnection()

    def getStatus(self):
        return self._layer.getStatus()