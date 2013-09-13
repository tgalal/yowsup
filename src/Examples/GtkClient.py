'''
Copyright (c) <2013> Pablo Castellano <pablo@anche.no>

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
from Yowsup.connectionmanager import YowsupConnectionManager
import time
import datetime
import sys
from gi.repository import Gtk
from gi.repository import GObject
GObject.threads_init()

if sys.version_info >= (3, 0):
    raw_input = input


class WhatsappGtkClient:

    def __init__(self, phoneNumber, keepAlive=False, sendReceipts=False):

        self.ui = Gtk.Builder()
        #self.ui.set_translation_domain(APP_NAME)
        self.ui.add_from_file('Examples/window.ui')
        self.ui.connect_signals(self)
        self.window = self.ui.get_object('window')
        self.window.connect('destroy', self.stop_loop)
        self.window.show_all()
        self.messagesbuffer = self.ui.get_object('messagesbuffer')
        self.debugbuffer = self.ui.get_object('debugbuffer')

        self.sendReceipts = sendReceipts
        self.phoneNumber = phoneNumber
        self.jid = "%s@s.whatsapp.net" % phoneNumber

        self.sentCache = {}

        connectionManager = YowsupConnectionManager()
        connectionManager.setAutoPong(keepAlive)
        self.signalsInterface = connectionManager.getSignalsInterface()
        self.methodsInterface = connectionManager.getMethodsInterface()

        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("message_received", self.onMessageReceived)
        self.signalsInterface.registerListener("receipt_messageSent", self.onMessageSent)
        self.signalsInterface.registerListener("presence_updated", self.onPresenceUpdated)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)

        self.commandMappings = {"lastseen": lambda: self.methodsInterface.call("presence_request", (self.jid,)),
                                "available": lambda: self.methodsInterface.call("presence_sendAvailable"),
                                "unavailable": lambda: self.methodsInterface.call("presence_sendUnavailable"),
                                "quit": lambda: self.stop_loop()
                                }

        self.done = False
        self.run_loop = True
        #signalsInterface.registerListener("receipt_messageDelivered", lambda jid, messageId: methodsInterface.call("delivered_ack", (jid, messageId)))

    def stop_loop(self, data=None):
        self.run_loop = False
        Gtk.main_quit()

    def login(self, username, password):
        self.username = username
        self.methodsInterface.call("auth_login", (username, password))
        Gtk.main()

        while not self.done:
            time.sleep(0.5)

    def onAuthSuccess(self, username):
        print("Authed %s" % username)
        self.methodsInterface.call("ready")
        self.goInteractive(self.phoneNumber)

    def onAuthFailed(self, username, err):
        print("Auth Failed!")

    def onDisconnected(self, reason):
        print("Disconnected because %s" % reason)

    def onPresenceUpdated(self, jid, lastSeen):
        formattedDate = datetime.datetime.fromtimestamp(long(time.time()) - lastSeen).strftime('%d-%m-%Y %H:%M')
        self.onMessageReceived(0, jid, "LAST SEEN RESULT: %s" % formattedDate, long(time.time()), False, None, False)

    def onMessageSent(self, jid, messageId):
        formattedDate = datetime.datetime.fromtimestamp(self.sentCache[messageId][0]).strftime('%d-%m-%Y %H:%M')
        line = "%s [%s]:%s" % (self.username, formattedDate, self.sentCache[messageId][1])
        print(line)
        line += "\n"
        self.messagesbuffer.insert_at_cursor(line, len(line))
        print(self.getPrompt())

    def runCommand(self, command):
        if command[0] == "/":
            command = command[1:].split(' ')
            try:
                self.commandMappings[command[0]]()
                return 1
            except KeyError:
                return 0

        return 0

    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadcast):
        if jid[:jid.index('@')] != self.phoneNumber:
            return
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        line = "%s [%s]:%s" % (jid, formattedDate, messageContent)
        print line
        line += "\n"
        self.messagesbuffer.insert_at_cursor(line, len(line))

        if wantsReceipt and self.sendReceipts:
            self.methodsInterface.call("message_ack", (jid, messageId))

        print(self.getPrompt())

    def goInteractive(self, jid):
        print("Starting Interactive chat with %s" % jid)
        jid = "%s@s.whatsapp.net" % jid
        print(self.getPrompt())
        while self.run_loop:
            message = raw_input()
            message = message.strip()
            if not len(message):
                continue
            if not self.runCommand(message.strip()):
                msgId = self.methodsInterface.call("message_send", (jid, message))
                self.sentCache[msgId] = [int(time.time()), message]
        self.done = True

    def getPrompt(self):
        return "Enter Message or command: (/%s)" % ", /".join(self.commandMappings)

    def write_to_debug_buffer(self, message, type):
        t = time.time()
        fmessage = "%s:\t%s" % (type, message)
	print fmessage
	self.debugbuffer.insert_at_cursor(fmessage, len(fmessage))
