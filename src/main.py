#!/usr/bin/python

'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

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

import os, re, json, anydbm as dbm
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import time, datetime, readline
import threading,time, base64

from Yowsup.Common.utilities import Utilities
from Yowsup.Common.debugger import Debugger
from Yowsup.Common.constants import Constants
from Examples.CmdClient import WhatsappCmdClient
from Examples.EchoClient import WhatsappEchoClient
from Examples.ListenerClient import WhatsappListenerClient
from Yowsup.Registration.v1.coderequest import WACodeRequest
from Yowsup.Registration.v1.regrequest import WARegRequest
from Yowsup.Registration.v1.existsrequest import WAExistsRequest
from Yowsup.Registration.v2.existsrequest import WAExistsRequest as WAExistsRequestV2
from Yowsup.Registration.v2.coderequest import WACodeRequest as WACodeRequestV2
from Yowsup.Registration.v2.regrequest import WARegRequest as WARegRequestV2
from Yowsup.connectionmanager import YowsupConnectionManager

CONFIG_PATH = os.path.expanduser("~/.whatsapp")
CONFIG_FILE = CONFIG_PATH + "/config.json"
ALIASES_FILE = CONFIG_PATH + "/aliases.db"

usage = """
  Whatsapp desktop client, interactive mode
  =========================================
  
  Destinations
  ------------
  There are two types of destinations:
  * Users can be addressed by their phone number (with country code and without any special 
    characters, e.g. 49179....)
  * Group chats can be addressed by prepending a # sign to the group chat id (e.g. #491...-130...)
  
  Sending messages
  ----------------
  Messages can be sent to a destination by typing:
    @DESTINATION: MESSAGE
  A default destination ca be set by typing:
    @DESTINATION
  Any text that is neither an @DESTINATION nor a command will be sent to the default destination.
  
  Aliases
  -------
  Instead of destination ids, the client can also use named aliases. If an alias exists for a
  destination id, it can be used instead of the destination id and it will be displayed on incoming
  messages.

  Commands
  --------
  All commands have the following form:
    !COMMAND PARAMETERS
  The following commands are recognized:
    !alias name=destination
      Assigns an alias to a destination (user or group), removes alias if destinatio is empty
    !aliases
      Displays all aliases
    !status user
      Determines the status of a user
    !group_create subject
      Creates a group with given subject
    !group_destroy group
      Destroys the group
    !group_invite group user
    
    !group_kick group user
    
    !group_subject group subject
    
    !group_members group
      Lists the group members
    !group_info group
      Retrieves information about a group
    !debug 1|0
      Enables/Disables debug mode
    !help
    !usage
      Displays this message
"""

def readConfig(path):
    with open(path) as fp:
        return json.load(fp)

def writeConfig(path, config):
    with open(path, "w") as fp:
        json.dump(config, fp, indent=2)

class WhatsappListenerClient:
    
    def __init__(self, configFile):
        self.configFile = configFile
        self.config = readConfig(self.configFile)
        self.aliases = dbm.open(ALIASES_FILE, "c")
        self._loadAliases()
        self.jid = "%s@s.whatsapp.net" % self.config["phone"]
        
        connectionManager = YowsupConnectionManager()
        connectionManager.setAutoPong(True)
        self.cm = connectionManager
        self.signalsInterface = connectionManager.getSignalsInterface()
        self.methodsInterface = connectionManager.getMethodsInterface()
        self.signalsInterface.registerListener("presence_updated", self.onPresenceUpdated)
        self.signalsInterface.registerListener("presence_available", self.onPresenceAvailable)
        self.signalsInterface.registerListener("presence_unavailable", self.onPresenceUnavailable)
        self.signalsInterface.registerListener("message_received", self.onMessageReceived)
        self.signalsInterface.registerListener("group_gotInfo", self.onGroupInfo)
        self.signalsInterface.registerListener("group_createSuccess", self.onGroupCreated)
        self.signalsInterface.registerListener("group_endSuccess", self.onGroupDestroyed)
        self.signalsInterface.registerListener("group_messageReceived", self.onGroupMessageReceived)
        self.signalsInterface.registerListener("group_subjectReceived", self.onGroupSubjectReceived)
        self.signalsInterface.registerListener("group_gotParticipants", self.onGroupGotParticipants)
        self.signalsInterface.registerListener("auth_success", self.onAuthSuccess)
        self.signalsInterface.registerListener("auth_fail", self.onAuthFailed)
        self.signalsInterface.registerListener("disconnected", self.onDisconnected)
        
        self.defaultReceiver = None
        self._login()
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self._complete)
        readline.set_completer_delims(" ")
    
    def close(self):
        self.aliases.close()
        self.methodsInterface.call("presence_sendUnavailable")
        
    def _complete(self, text, nr):
        tokens = ["!help", "!usage", "!status", "!debug", "!alias", "!aliases", "!group_create",
                  "!group_destroy", "!group_invite", "!group_kick", "!group_members", "!group_info",
                  "!group_subject"]
        for alias in self.aliases:
            tokens.append("@%s:" % alias)
            tokens.append(alias)
        matching = filter(lambda t: t.startswith(text), tokens)
        return matching[nr] if len(matching) >= nr else None
        
    def _loadAliases(self):
        self.aliasesRev = dict([(v, k) for (k, v) in self.aliases.iteritems()])
    
    def _login(self):
        self.username = self.config["phone"]
        password = base64.b64decode(self.config["password"])
        self.methodsInterface.call("auth_login", (self.username, password))

    def _name2jid(self, name):
        if name in self.aliases:
            name = self.aliases[name]
        if name.startswith("#"):
            return "%s@g.us" % name[1:]
        else:
            return "%s@s.whatsapp.net" % name

    def _jid2name(self, jid):
        name, server = jid.split("@")
        if server == "g.us":
            name = "#" + name
        if name in self.aliasesRev:
            name = self.aliasesRev[name]
        return name
        
    def _alias(self, alias, name):
        self.aliases[alias] = name
        if not name:
            del self.aliases[alias]
        self._loadAliases()

    def onAuthSuccess(self, username):
        print "Logged in as %s" % username
        self.methodsInterface.call("ready")
        self.methodsInterface.call("presence_sendAvailable")

    def onAuthFailed(self, username, err):
        print "Auth Failed!"

    def onDisconnected(self, reason):
        print "Disconnected because %s" %reason
        try:
            self._login()
        except:
            pass

    def onGroupInfo(self, jid, owner, subject, subjectOwner, subjectTimestamp, creationTimestamp):
        creationTimestamp = datetime.datetime.fromtimestamp(creationTimestamp).strftime('%d-%m-%Y %H:%M')
        subjectTimestamp = datetime.datetime.fromtimestamp(subjectTimestamp).strftime('%d-%m-%Y %H:%M')
        print "Information on group %s: created by %s at %s, subject '%s' set by %s at %s" % (self._jid2name(jid), self._jid2name(owner), creationTimestamp, subject, self._jid2name(subjectOwner), subjectTimestamp)
            
    def onGroupCreated(self, jid, groupJid):
        groupJid = "%s@%s" % (groupJid, jid) 
        print "New group: %s" % self._jid2name(groupJid)
            
    def onGroupDestroyed(self, jid):
        pass #jid contains only "g.us" ????

    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        print "[%s] %s: %s"%(formattedDate, self._jid2name(jid), messageContent)
        if wantsReceipt:
            self.methodsInterface.call("message_ack", (jid, messageId))
            
    def onGroupMessageReceived(self, messageId, jid, author, messageContent, timestamp, wantsReceipt, pushName):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        print "[%s] %s -> %s: %s"%(formattedDate, self._jid2name(author), self._jid2name(jid), messageContent)
        if wantsReceipt:
            self.methodsInterface.call("message_ack", (jid, messageId))
            
    def onGroupSubjectReceived(self, messageId, jid, author, subject, timestamp, wantsReceipt, pushName):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        print "[%s] %s changed subject of %s to '%s'" % (formattedDate, self._jid2name(author), self._jid2name(jid), subject)
        if wantsReceipt:
            self.methodsInterface.call("subject_ack", (jid, messageId))

    def onGroupGotParticipants(self, groupJid, participants):
        print "Members of group %s: %s" % (self._jid2name(groupJid), [self._jid2name(p) for p in participants])
            
    def _send(self, receiver, msg):
        if not "@" in receiver:
           receiver = self._name2jid(receiver)
        self.methodsInterface.call("message_send", (receiver, msg))
            
    def _cmd(self, cmd, args):
        if cmd == "alias":
           alias, name = (" ".join(args)).split("=")
           self._alias(alias, name)           
        elif cmd == "aliases":
           print ", ".join(["%s=%s" % (k, v) for k, v in self.aliases.iteritems()])
        elif cmd == "group_info":
           self.methodsInterface.call("group_getInfo", (self._name2jid(args[0]),))
        elif cmd == "group_invite":
           self.methodsInterface.call("group_addParticipant", (self._name2jid(args[0]), self._name2jid(args[1])))
        elif cmd == "group_kick":
           self.methodsInterface.call("group_removeParticipant", (self._name2jid(args[0]), self._name2jid(args[1])))
        elif cmd == "group_create":
           self.methodsInterface.call("group_create", (args[0],))
        elif cmd == "group_destroy":
           self.methodsInterface.call("group_end", (self._name2jid(args[0]),))
        elif cmd == "group_subject":
           self.methodsInterface.call("group_subject", (self._name2jid(args[0]), args[0]))
        elif cmd == "group_members":
           self.methodsInterface.call("group_getParticipants", (self._name2jid(args[0]),))
        elif cmd == "status":
           self.methodsInterface.call("presence_request", (self._name2jid(args[0]),))
        elif cmd == "debug":
           Debugger.enabled = args[0].lower() in ["true", "1", "yes"]
        elif cmd == "help" or cmd == "usage":
           print usage
        
    def onPresenceUpdated(self, jid, lastseen):
        print "%s was last seen %s seconds ago" % (self._jid2name(jid), lastseen)
        
    def onPresenceAvailable(self, jid):
        print "%s is now available" % self._jid2name(jid)
        
    def onPresenceUnavailable(self, jid):
        print "%s is now unavailable" % self._jid2name(jid)

    def run(self):
        while True:
            line = raw_input("@%s:> " % (self.defaultReceiver or "???"))
            if line.startswith("!"):
                args = line[1:].split(" ")
                self._cmd(args[0], args[1:])
                continue
            match = re.match("@([^:]*):[ ]*(.*)", line)
            if match:
                addr, msg = match.groups()
                self._send(addr, msg)
                continue
            match = re.match("@([^:]*)", line)
            if match:
                addr = match.groups()[0]
                self.defaultReceiver = addr
                continue
            if line and self.defaultReceiver:
                msg = line.strip()
                self._send(self.defaultReceiver, msg)
                continue
            print "Warning: line ignored (type !usage to see a help message)"

def configure(CONFIG_FILE):
    phoneNumber = raw_input("Phone number (without country code, no leading 0): ")
    countryCode = raw_input("Country code (no leading +): ")
    phone = countryCode + phoneNumber
    password = raw_input("Password (base64 encoded, leave empty to register): ")
    if not password:
        identity = raw_input("Identity (leave empty if unknown): ") or "0000000000"
        method = raw_input("Verification method (sms or voice): ") or "sms"
        req = WACodeRequestV2(countryCode, phoneNumber, identity, method)
        res = req.send()
        print "-"*25
        print res
        print "-"*25
        code = raw_input("Received verification code: ")
        code = "".join(code.split('-'))
        req = WARegRequestV2(countryCode, phoneNumber, code, identity)
        res = req.send()
        print "-"*25
        print res
        print "-"*25
        password = res["pw"]
    config = {"phone": phone, "password": password}
    writeConfig(CONFIG_FILE, config)
                     
if __name__ == "__main__":
    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
    if not os.path.exists(CONFIG_FILE):
        configure(CONFIG_FILE)
    wa = WhatsappListenerClient(CONFIG_FILE)
    try:
        wa.run()
    except:
        wa.close()
