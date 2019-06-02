from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
import threading, _thread


class RecieverLayer(YowInterfaceLayer):

    def __init__(self):
        super(RecieverLayer, self).__init__()
        # Set 5 seconds to recieve some messages
        threading.Timer(5.0, self.end).start()

    def end(self):
        print("Timeout reached")
        _thread.interrupt_main()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        print("Message:{from:%s,text:\"%s\"}" % (messageProtocolEntity.getFrom(False), messageProtocolEntity.getBody()))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.media_type == "image":
            print("Image:{from:%s,url:\"%s\"}" % (messageProtocolEntity.getFrom(False), messageProtocolEntity.url))

        # Issue: AttributeError: 'LocationMediaMessageProtocolEntity' object has no attribute 'getLatitude'
        # elif messageProtocolEntity.media_type == "location":
        #     print("Location:from:%s;lat:%s,lng:%s" % (messageProtocolEntity.getFrom(False), messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude()))

        # Issue: Unsupported mediatype: vcard, will send receipts
        # elif messageProtocolEntity.media_type == "contact":
        #     print("Contact:from:%s;name:%s;card:%s" % (messageProtocolEntity.getFrom(False), messageProtocolEntity.getName(), messageProtocolEntity.getCardData()))
