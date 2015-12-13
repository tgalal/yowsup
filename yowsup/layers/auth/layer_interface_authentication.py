from yowsup.layers import YowLayerInterface

class YowAuthenticationProtocolLayerInterface(YowLayerInterface):
    def setCredentials(self, phone, password):
        self._layer.setCredentials((phone, password))

    def getUsername(self, full = False):
        return self._layer.getUsername(full)
