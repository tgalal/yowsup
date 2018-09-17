from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_media.protocolentities.iq_requestupload import RequestUploadIqProtocolEntity
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers.auth.protocolentities import StreamErrorProtocolEntity
from yowsup.layers import EventCallback
import inspect
import logging
logger = logging.getLogger(__name__)


class ProtocolEntityCallback(object):
    def __init__(self, entityType):
        self.entityType = entityType

    def __call__(self, fn):
        fn.entity_callback = self.entityType
        return fn


class YowInterfaceLayer(YowLayer):

    PROP_RECONNECT_ON_STREAM_ERR = "org.openwhatsapp.yowsup.prop.interface.reconnect_on_stream_error"

    def __init__(self):
        super(YowInterfaceLayer, self).__init__()
        self.reconnect = False
        self.entity_callbacks = {}
        self.iqRegistry = {}
        # self.receiptsRegistry = {}
        members = inspect.getmembers(self, predicate=inspect.ismethod)
        for m in members:
            if hasattr(m[1], "entity_callback"):
                fname = m[0]
                fn = m[1]
                self.entity_callbacks[fn.entity_callback] = getattr(self, fname)

    def _sendIq(self, iqEntity, onSuccess=None, onError=None):
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

                if entity.getType() == IqProtocolEntity.TYPE_RESULT and successClbk:
                    successClbk(entity, originalIq)
                elif entity.getType() == IqProtocolEntity.TYPE_ERROR and errorClbk:
                    errorClbk(entity, originalIq)
                return True

        return False

    def getOwnJid(self, full=True):
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

    @ProtocolEntityCallback("stream:error")
    def onStreamError(self, streamErrorEntity):
        logger.error(streamErrorEntity)
        if self.getProp(self.__class__.PROP_RECONNECT_ON_STREAM_ERR, True):
            if streamErrorEntity.getErrorType() == StreamErrorProtocolEntity.TYPE_CONFLICT:
                logger.warn("Not reconnecting because you signed in in another location")
            else:
                logger.info("Initiating reconnect")
                self.reconnect = True
        else:
            logger.warn("Not reconnecting because property %s is not set" %
                        self.__class__.PROP_RECONNECT_ON_STREAM_ERR)
        self.toUpper(streamErrorEntity)
        self.disconnect()

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, yowLayerEvent):
        self.reconnect = False

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onDisconnected(self, yowLayerEvent):
        if self.reconnect:
            self.reconnect = False
            self.connect()

    def _sendMediaMessage(self, builder, success, error=None, progress=None):
        # axolotlIface = self.getLayerInterface(YowAxolotlLayer)
        # if axolotlIface:
        #     axolotlIface.encryptMedia(builder)

        iq = RequestUploadIqProtocolEntity(
            builder.mediaType, filePath=builder.getFilepath(), encrypted=builder.isEncrypted())

        def successFn(resultEntity, requestUploadEntity): return self.__onRequestUploadSuccess(
            resultEntity, requestUploadEntity, builder, success, error, progress)

        def errorFn(errorEntity, requestUploadEntity): return self.__onRequestUploadError(
            errorEntity, requestUploadEntity, error)
        self._sendIq(iq, successFn, errorFn)

    def __onRequestUploadSuccess(self, resultRequestUploadIqProtocolEntity, requestUploadEntity, builder, success, error=None, progress=None):
        if(resultRequestUploadIqProtocolEntity.isDuplicate()):
            return success(builder.build(resultRequestUploadIqProtocolEntity.getUrl(), resultRequestUploadIqProtocolEntity.getIp()))
        else:
            def successFn(path, jid, url): return self.__onMediaUploadSuccess(
                builder, url, resultRequestUploadIqProtocolEntity.getIp(), success)

            def errorFn(path, jid, errorText): return self.__onMediaUploadError(
                builder, errorText, error)

            mediaUploader = MediaUploader(builder.jid, self.getOwnJid(), builder.getFilepath(),
                                          resultRequestUploadIqProtocolEntity.getUrl(),
                                          resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                          successFn, errorFn, progress, asynchronous=True)
            mediaUploader.start()

    def __onRequestUploadError(self, errorEntity, requestUploadEntity, builder, error=None):
        if error:
            return error(errorEntity.code, errorEntity.text, errorEntity.backoff)

    def __onMediaUploadSuccess(self, builder, url, ip, successClbk):
        messageNode = builder.build(url, ip)
        return successClbk(messageNode)

    def __onMediaUploadError(self, builder, errorText, errorClbk=None):
        if errorClbk:
            return errorClbk(0, errorText, 0)

    def __str__(self):
        return "Interface Layer"
