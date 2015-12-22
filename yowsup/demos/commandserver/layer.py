import os
import string
import subprocess
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback

class CommandServerLayer(YowInterfaceLayer):
	
    def executeCommand(self, messageProtocolEntity, command):
	status = subprocess.check_output(command)
	print("Status: "+status)
	messageProtocolEntity.setBody(status)
	self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))

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
        # Execute command if possible.
        if string.lower(messageProtocolEntity.getBody())=="ls":
		command = ['ls', '-l']
		self.executeCommand(messageProtocolEntity, command)
        elif string.lower(messageProtocolEntity.getBody())=="reboot":
		command = ['sudo', 'reboot']
                self.executeCommand(messageProtocolEntity, command)
        else:
                # just print info
                print("Invalid command '%s' from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
		messageProtocolEntity.setBody("Invalid command '%s'." % messageProtocolEntity.getBody() )
                self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        #os.system("notify-send 'Mensaje de Whatsapp' '{mensje}'".format(mensje=messageProtocolEntity.getBody()))

    def onMediaMessage(self, messageProtocolEntity):
        # just print info
        if messageProtocolEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (messageProtocolEntity.getLatitude(), messageProtocolEntity.getLongitude(), messageProtocolEntity.getFrom(False)))

        elif messageProtocolEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (messageProtocolEntity.getName(), messageProtocolEntity.getCardData(), messageProtocolEntity.getFrom(False)))

	#Echo message
	self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))