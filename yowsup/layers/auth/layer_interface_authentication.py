from yowsup.layers import YowLayerInterface

class YowAuthenticationProtocolLayerInterface(YowLayerInterface):
    def setCredentials(self, phone, keypair):
        self._layer.setCredentials((phone, keypair))

    def getUsername(self, full = False):
        return self._layer.getUsername(full)
