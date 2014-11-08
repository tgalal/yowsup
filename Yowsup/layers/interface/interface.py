from Yowsup.layers import YowLayer, YowLayerEvent
class YowInterfaceLayer(YowLayer):

    def connect(self):
        loginEvent = YowLayerEvent("network.state.connect")
        self.broadcastEvent(loginEvent)

    def send(self, data):
        self.toLower(data)

    def receive(self, entity):
        if entity.isType("success"):
            print(entity.status)
            print(entity.kind)
            print(entity.expiration)


    def __str__(self):
        return "Interface Layer"