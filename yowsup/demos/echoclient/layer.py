from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_receipts.protocolentities  import OutgoingReceiptProtocolEntity
from yowsup.layers.protocol_media.protocolentities  import LocationMediaMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities      import OutgoingAckProtocolEntity



class EchoLayer(YowInterfaceLayer):

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if not messageProtocolEntity.isGroupMessage():
            if messageProtocolEntity.getType() == 'text':
                self.onTextMessage(messageProtocolEntity)
            elif messageProtocolEntity.getType() == 'media':
                self.onMediaMessage(messageProtocolEntity)
    
    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt", "delivery")
        self.toLower(ack)

    def onTextMessage(self,messageProtocolEntity):
        receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())
            
        outgoingMessageProtocolEntity = TextMessageProtocolEntity(
            messageProtocolEntity.getBody(),
            to = messageProtocolEntity.getFrom())

        print("Echoing %s to %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))

        #send receipt otherwise we keep receiving the same message over and over
        self.toLower(receipt)
        self.toLower(outgoingMessageProtocolEntity)

    def onMediaMessage(self, messageProtocolEntity):
        if messageProtocolEntity.getMediaType() == "image":
            
            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

            outImage = ImageDownloadableMediaMessageProtocolEntity(
                messageProtocolEntity.getMimeType(), messageProtocolEntity.fileHash, messageProtocolEntity.url, messageProtocolEntity.ip,
                messageProtocolEntity.size, messageProtocolEntity.fileName, messageProtocolEntity.encoding, messageProtocolEntity.width, messageProtocolEntity.height,
                messageProtocolEntity.getCaption(),
                to = messageProtocolEntity.getFrom(), preview = messageProtocolEntity.getPreview())

            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(receipt)
            self.toLower(outImage)

        elif messageProtocolEntity.getMediaType() == "location":

            receipt = OutgoingReceiptProtocolEntity(messageProtocolEntity.getId(), messageProtocolEntity.getFrom())

            outLocation = LocationMediaMessageProtocolEntity(messageProtocolEntity.getLatitude(),
                messageProtocolEntity.getLongitude(), messageProtocolEntity.getLocationName(),
                messageProtocolEntity.getLocationURL(), messageProtocolEntity.encoding,
                to = messageProtocolEntity.getFrom(), preview=messageProtocolEntity.getPreview())

            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

            #send receipt otherwise we keep receiving the same message over and over
            self.toLower(outLocation)
            self.toLower(receipt)

 
