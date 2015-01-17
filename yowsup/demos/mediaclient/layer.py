import os
import sys
import logging

from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_media.protocolentities import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.common import MediaDiscover


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SendMediaLayer(YowInterfaceLayer):
    PROP_MESSAGES = 'org.openwhatsapp.yowsup.prop.sendclient.queue'  # list of (jid, path) tuples

    def __init__(self):
        super(SendMediaLayer, self).__init__()
        self.MEDIA_TYPE = None
        self.ackQueue = []

    def disconnect(self):
        self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))

    @ProtocolEntityCallback('success')
    def onSuccess(self, entity):
        self.main()

    @ProtocolEntityCallback('ack')
    def onAck(self, entity):
        if entity.getId() in self.ackQueue:
            self.ackQueue.pop(self.ackQueue.index(entity.getId()))

        if not len(self.ackQueue):
            logger.info('Message sent')
            self.disconnect()

    def onRequestUploadResult(self, jid, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        if resultRequestUploadIqProtocolEntity.isDuplicate():
            if self.MEDIA_TYPE == "image":
                self.doSendImage(filePath, resultRequestUploadIqProtocolEntity.getUrl(),
                                 jid, resultRequestUploadIqProtocolEntity.getIp())
            elif self.MEDIA_TYPE == "video":
                self.doSendVideo(filePath, resultRequestUploadIqProtocolEntity.getUrl(),
                                 jid, resultRequestUploadIqProtocolEntity.getIp())
            elif self.MEDIA_TYPE == "audio":
                self.doSendAudio(filePath, resultRequestUploadIqProtocolEntity.getUrl(),
                                 jid, resultRequestUploadIqProtocolEntity.getIp())
        else:
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                          resultRequestUploadIqProtocolEntity.getUrl(),
                                          resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                          self.onUploadSuccess, self.onUploadError, self.onUploadProgress, async=False)

            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))
        self.disconnect()

    def onUploadSuccess(self, filePath, jid, url):
        if self.MEDIA_TYPE == "image":
            self.doSendImage(filePath, url, jid)
        elif self.MEDIA_TYPE == "video":
            self.doSendVideo(filePath, url, jid)
        elif self.MEDIA_TYPE == "audio":
            self.doSendAudio(filePath, url, jid)

    def onUploadError(self, filePath, jid, url):
        logger.error("Request upload for file %s for %s failed" % (filePath, jid))
        self.disconnect()

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def doSendImage(self, filePath, url, to, ip=None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        self.toLower(entity)

    def doSendVideo(self, filePath, url, to, ip=None):
        #  fpath, url, mediaType, ip, to, mimeType = None, preview = None, filehash = None, filesize = None
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, "video", ip, to)
        self.toLower(entity)

    def doSendAudio(self, filePath, url, to, ip=None):
        #  fpath, url, mediaType, ip, to, mimeType = None, preview = None, filehash = None, filesize = None
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, "audio", ip, to)
        self.toLower(entity)

    def main(self):
        for target in self.getProp(self.__class__.PROP_MESSAGES, []):
            jid, path = target
            jid = '%s@s.whatsapp.net' % jid
            self.MEDIA_TYPE = MediaDiscover.getMediaType(path)

            if self.MEDIA_TYPE is None:
                logger.debug("Media not recognized")
                self.disconnect()

            logger.debug("Send %s in %s to %s" % (self.MEDIA_TYPE, path, jid))

            entity = None
            if self.MEDIA_TYPE == "image":
                entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE, filePath=path)
            elif self.MEDIA_TYPE == "video":
                entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO, filePath=path)
            elif self.MEDIA_TYPE == "audio":
                entity = RequestUploadIqProtocolEntity(RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO, filePath=path)

            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, path,
                                                                                         successEntity, originalEntity)

            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path,
                                                                                    errorEntity, originalEntity)
            self._sendIq(entity, successFn, errorFn)
