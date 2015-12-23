import os
import string
import subprocess
from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback

#Users that can execute commands. The complete user name is printed in console when not allowed. Copy to this array, 
allowed_users = ['34666888999@s.whatsapp.net']

class CommandServerLayer(YowInterfaceLayer):

    #Executes a command if the user is in the allowed_user list. 
    def executeCommand(self, messageProtocolEntity, command):	
        if messageProtocolEntity.getFrom() in allowed_users:	    
            status = subprocess.check_output(command)
            print("Status: "+status)
            messageProtocolEntity.setBody(status)
        else:
            print("Not allowed user '%s'" % messageProtocolEntity.getFrom())
            messageProtocolEntity.setBody("Authorization check failed!")
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

    #Media messages cannot send commands. 
    def onMediaMessage(self, messageProtocolEntity):
       # do nothing. 
       return
