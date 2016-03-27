from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import IncomingAckProtocolEntity
from yowsup.layers.axolotl.layer import YowAxolotlLayer
from yowsup.layers.protocol_media.protocolentities.iq_requestupload import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.protocolentities.iq_requestupload_result import ResultRequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.axolotl.layer import YowAxolotlLayer
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

    def _sendMediaMessage(self, builder, success, error = None, progress = None):
        # axolotlIface = self.getLayerInterface(YowAxolotlLayer)
        # if axolotlIface:
        #     axolotlIface.encryptMedia(builder)

        iq = RequestUploadIqProtocolEntity(builder.mediaType, filePath = builder.getFilepath(), encrypted = builder.isEncrypted())
        successFn = lambda resultEntity, requestUploadEntity: self.__onRequestUploadSuccess(resultEntity, requestUploadEntity, builder, success, error, progress)
        errorFn = lambda errorEntity, requestUploadEntity: self.__onRequestUploadError(errorEntity, requestUploadEntity, error)
        self._sendIq(iq, successFn, errorFn)

    def __onRequestUploadSuccess(self, resultRequestUploadIqProtocolEntity, requestUploadEntity, builder, success, error = None, progress = None):
        if(resultRequestUploadIqProtocolEntity.isDuplicate()):
            return success(builder.build(resultRequestUploadIqProtocolEntity.getUrl(), resultRequestUploadIqProtocolEntity.getIp()))
        else:
            successFn = lambda path, jid, url: self.__onMediaUploadSuccess(builder, url, resultRequestUploadIqProtocolEntity.getIp(), success)
            errorFn = lambda path, jid, errorText: self.__onMediaUploadError(builder, errorText, error)

            mediaUploader = MediaUploader(builder.jid, self.getOwnJid(), builder.getFilepath(),
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, errorFn, progress, async=True)
            mediaUploader.start()

    def __onRequestUploadError(self, errorEntity, requestUploadEntity, builder, error = None):
        if error:
            return error(errorEntity.code, errorEntity.text, errorEntity.backoff)

    def __onMediaUploadSuccess(self, builder, url, ip, successClbk):
        messageNode = builder.build(url, ip)
        return successClbk(messageNode)

    def __onMediaUploadError(self, builder, errorText, errorClbk = None):
        if errorClbk:
            return errorClbk(0, errorText, 0)

    def __str__(self):
        return "Interface Layer"
