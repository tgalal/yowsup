from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
import uuid
import logging
logger = logging.getLogger(__name__)

class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        logger.info("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):

        if not os.path.exists("/tmp/yowfiles"):
            os.makedirs("/tmp/yowfiles")

        # set unique filename
        uniqueFilename = "/tmp/yowfiles/%s-%s%s" % (messageProtocolEntity.getFrom(False), uuid.uuid4().hex, messageProtocolEntity.getExtension())

        if messageProtocolEntity.getMediaType() == "image":
            logger.info("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open(uniqueFilename, 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "video":
            logger.info("Echoing video %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open(uniqueFilename, 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "audio":
            logger.info("Echoing audio %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open(uniqueFilename, 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "document":
            logger.info("Echoing document %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open(uniqueFilename, 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "location":
            logger.info("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))
        elif messageProtocolEntity.getMediaType() == "vcard":
            logger.info("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))
