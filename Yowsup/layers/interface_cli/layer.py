from Yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from Yowsup.layers.messages.protocolentities import TextMessageProtocolEntity
import threading, sys
class YowCliInterfaceLayer(YowInterfaceLayer):

    def __init__(self):
        super(YowCliInterfaceLayer, self).__init__()
        self.commandMappings = {}

    def startInputThread(self):
        jid = "4915225256022@s.whatsapp.net"
        notify = "Self",
        print("Starting Interactive chat with %s" % jid)
        while(True):
            message = raw_input().strip()
            if len(message):
                if not self.runCommand(message):
                    # _id, _from, timestamp, notify, body, participant = None, offline = False, retry = None)
                    outgoingMessage = TextMessageProtocolEntity(message, to = jid)
                    print(outgoingMessage)
                    print(outgoingMessage.toProtocolTreeNode())
                    self.toLower(outgoingMessage)


    def getPrompt(self):
        return "Enter Message or command: (/%s)" % ", /".join(self.commandMappings)


    def runCommand(self, command):
        if command[0] == "/":
            command = command[1:].split(' ')
            try:
                self.commandMappings[command[0]]()
                return 1
            except KeyError:
                return 0
        
        return 0


    def goInteractive(self, jid):
        print("Starting Interactive chat with %s" % jid)
        jid = "%s@s.whatsapp.net" % jid
        print(self.getPrompt())
        while True:
            message = raw_input()
            message = message.strip()
            if not len(message):
                continue
            if not self.runCommand(message.strip()):
                msgId = self.methodsInterface.call("message_send", (jid, message))
                self.sentCache[msgId] = [int(time.time()), message]
        self.done = True

    def send(self, data):
        self.toLower(data)

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        print("Logged In")
        t = threading.Thread(target = self.startInputThread)
        t.daemon = True
        t.start()

    @ProtocolEntityCallback("message")
    def onMessage(self, messageEntity):
        print("Message Received")
        print(messageEntity)
        

    def __str__(self):
        return "CLI Interface Layer"

