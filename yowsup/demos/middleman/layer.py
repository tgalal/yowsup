from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity

class MiddleManLayer(YowInterfaceLayer):
    PROP_GROUPS = "org.openwhatsapp.yowsup.prop.sendclient.queue"

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

#print messageProtocolEntity
# grp1 = '919429818384-1449249364@g.us'
# grp2 = '919904773407-1449240031@g.us'
# configFile = open("/middleman.config",'r')
# tempStr = configFile.readlines()
# grp1 = tempStr[0]
# grp2 = tempStr[1]
# configFile.close()
        groups = self.getProp(self.__class__.PROP_GROUPS, [])
        grp1 = groups[0]
        # print grp1
        grp2 = groups[1]
        # print grp2
        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        sender = messageProtocolEntity.getParticipant().split('@')[0] + " says:"

        if messageProtocolEntity.getFrom() == grp1:
            if messageProtocolEntity.getType() == 'text':
                messageProtocolEntity.setBody(sender + messageProtocolEntity.getBody())
            else:
                newmessage = TextMessageProtocolEntity(sender, to = grp2)
                self.toLower(newmessage)
            self.toLower(messageProtocolEntity.forward(grp2))
            self.toLower(messageProtocolEntity.ack())
            self.toLower(messageProtocolEntity.ack(True))

        elif messageProtocolEntity.getFrom() == grp2:
            if messageProtocolEntity.getType() == 'text':
                messageProtocolEntity.setBody(sender + messageProtocolEntity.getBody())
            else:
                newmessage = TextMessageProtocolEntity(sender, to = grp1)
            self.toLower(newmessage)
            self.toLower(messageProtocolEntity.forward(grp1))
            self.toLower(messageProtocolEntity.ack())
            self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self,messageProtocolEntity):
        # just print info
        print("Sending this message %s from %s to %s" % (messageProtocolEntity.getBody(),messageProtocolEntity.getParticipant(), messageProtocolEntity.getFrom(False)))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Sending image %s from %s to %s" % (messageProtocolEntity.url,messageProtocolEntity.getParticipant(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Sending location (%s, %s) form %s to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(),messageProtocolEntity.getParticipant(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Sending vcard (%s, %s) form %s to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(),messageProtocolEntity.getParticipant(), messageProtocolEntity.getFrom(False)))
