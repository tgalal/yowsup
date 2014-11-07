from Yowsup.layers import YowLayer, YowLayerEvent
class YowInterfaceLayer(YowLayer):

    def connect(self):
        loginEvent = YowLayerEvent("network.state.connect")
        self.broadcastEvent(loginEvent)

    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        self.toUpper(data)

    def __str__(self):
        return "Interface Layer"