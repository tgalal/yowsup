from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import IncomingAckProtocolEntity
import inspect

class ProtocolEntityCallback(object):
    def __init__(self, entityType):
        self.entityType = entityType

    def __call__(self, fn):
        fn.entity_callback = self.entityType
        return fn
    

class YowInterfaceLayer(YowLayer):

    def __init__(self):
        super(YowInterfaceLayer, self).__init__()
        self.entity_callbacks = {}
        self.iqRegistry = {}
        # self.receiptsRegistry = {}
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for m in members:
            if hasattr(m[1], "entity_callback"):
                fname = m[0]
                fn = m[1]
                self.entity_callbacks[fn.entity_callback] = getattr(self, fname)
            

    def _sendIq(self, iqEntity, onSuccess = None, onError = None):
        assert iqEntity.getTag() == "iq", "Expected *IqProtocolEntity in _sendIq, got %s" % iqEntity.getTag()
        self.iqRegistry[iqEntity.getId()] = (iqEntity, onSuccess, onError)
        self.toLower(iqEntity)

    # def _sendReceipt(self, outgoingReceiptProtocolEntity, onAck = None):
    #     assert outgoingReceiptProtocolEntity.__class__ == OutgoingReceiptProtocolEntity,\
    #         "Excepted OutgoingReceiptProtocolEntity in _sendReceipt, got %s" % outgoingReceiptProtocolEntity.__class__
    #     self.receiptsRegistry[outgoingReceiptProtocolEntity.getId()] = (outgoingReceiptProtocolEntity, onAck)
    #     self.toLower(outgoingReceiptProtocolEntity)

    # def processReceiptsRegistry(self, incomingAckProtocolEntity):
    #     '''
    #     entity: IncomingAckProtocolEntity
    #     '''
    #
    #     if incomingAckProtocolEntity.__class__ != IncomingAckProtocolEntity:
    #         return False
    #
    #     receipt_id = incomingAckProtocolEntity.getId()
    #     if receipt_id in self.receiptsRegistry:
    #         originalReceiptEntity, ackClbk = self.receiptsRegistry[receipt_id]
    #         del self.receiptsRegistry[receipt_id]
    #
    #         if ackClbk:
    #             ackClbk(incomingAckProtocolEntity, originalReceiptEntity)
    #
    #         return True
    #
    #     return False


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
        return self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(full)

    def connect(self):
        self.getLayerInterface(YowNetworkLayer).connect()

    def disconnect(self):
        disconnectEvent = YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT)
        self.broadcastEvent(disconnectEvent)

    def send(self, data):
        self.toLower(data)

    def receive(self, entity):
        if not self.processIqRegistry(entity):
            entityType = entity.getTag()
            if entityType in self.entity_callbacks:
                self.entity_callbacks[entityType](entity)
            else:
                self.toUpper(entity)
 
    def __str__(self):
        return "Interface Layer"
