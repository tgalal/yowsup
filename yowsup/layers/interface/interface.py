from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
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
        self.iqRegistry = {}
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for m in members:
            if hasattr(m[1], "callback"):
                fname = m[0]
                fn = m[1]
                self.callbacks[fn.callback] = getattr(self, fname)

    def _sendIq(self, iqEntity, onSuccess = None, onError = None):
        assert iqEntity.getTag() == "iq", "Expected *IqProtocolEntity in _sendIq, got %s" % iqEntity.getTag()
        self.iqRegistry[iqEntity.getId()] = (iqEntity, onSuccess, onError)
        self.toLower(iqEntity)

    def processIqRegistry(self, entity):
        """
        :type entity: IqProtocolEntity
        """
        if entity.getTag() == "iq":
            iq_id = entity.getId()
            if iq_id in self.iqRegistry:
                originalIq, successClbk, errorClbk = self.iqRegistry[iq_id]
                del self.iqRegistry[iq_id]

                if entity.getType() ==  IqProtocolEntity.TYPE_RESULT and successClbk:
                    successClbk(entity, originalIq)
                elif entity.getType() == IqProtocolEntity.TYPE_ERROR and errorClbk:
                    errorClbk(entity, originalIq)
                return True

        return False

    def getOwnJid(self, full = True):
        jid = self.getProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS)[0]
        if jid:
            return jid + "@s.whatsapp.net" if full else jid
        return None

    def connect(self):
        loginEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT)
        self.broadcastEvent(loginEvent)

    def disconnect(self):
        disconnectEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT)
        self.broadcastEvent(disconnectEvent)

    def send(self, data):
        self.toLower(data)

    def receive(self, entity):
        if not self.processIqRegistry(entity):
            entityType = entity.getTag()
            if entityType in self.callbacks:
                self.callbacks[entityType](entity)
        

    def __str__(self):
        return "Interface Layer"

