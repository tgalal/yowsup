from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback

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
        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        if not os.path.exists("/tmp/yowfiles"):
            os.makedirs("/tmp/yowfiles")
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open("/tmp/yowfiles/%s%s" % (self.generateIdentity(), messageProtocolEntity.getExtension()), 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "video":
            print("Echoing video %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open("/tmp/yowfiles/%s%s" % (self.generateIdentity(), messageProtocolEntity.getExtension()), 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "audio":
            print("Echoing audio %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open("/tmp/yowfiles/%s%s" % (self.generateIdentity(), messageProtocolEntity.getExtension()), 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "document":
            print("Echoing document %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            data = messageProtocolEntity.getMediaContent()
            f = open("/tmp/yowfiles/%s" % (messageProtocolEntity.getFileName()), 'wb')
            f.write(data)
            f.close()
        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

