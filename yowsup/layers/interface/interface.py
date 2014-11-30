from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
import inspect

class ProtocolEntityCallback(object):
    def __init__(self, entityType):
        self.entityType = entityType

    def __call__(self, fn):
        fn.callback = self.entityType
        return fn

class YowInterfaceLayer(YowLayer):

    def __init__(self):
        self.callbacks = {}
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for m in members:
            if hasattr(m[1], "callback"):
                fname = m[0]
                fn = m[1]
                self.callbacks[fn.callback] = getattr(self, fname)

    def connect(self):
        loginEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)
        self.broadcastEvent(loginEvent)

    def disconnect(self):
        disconnectEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT)
        self.broadcastEvent(disconnectEvent)

    def send(self, data):
        self.toLower(data)

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        print("Logged in")

    def receive(self, entity):
        entityType = entity.getTag()
        if entityType in self.callbacks:
            self.callbacks[entityType](entity)
        

    def __str__(self):
        return "Interface Layer"

