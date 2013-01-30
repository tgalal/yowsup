#!/usr/bin/python

import os, re, json
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir)
import time, datetime, readline, cmd
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
ALIASES_FILE = CONFIG_PATH + "/aliases.json"
LOG_FILE = CONFIG_PATH + "/chat.log"

GENERAL_DOC = """
Whatsapp desktop client, interactive mode
=========================================
Type '/help send' to get information on sending messages.
Type '/help alias' to get information on using aliases.
Commands can be invoked by typing '/CMD' where CMD is one of the following.
Type '/help CMD' to get help on a command.  
"""

def readJSON(path):
    with open(path) as fp:
        return json.load(fp)

def writeJSON(path, config):
    with open(path, "w") as fp:
        json.dump(config, fp, indent=2)

_eventBindings = {}
    
def bind(event):
    def wrap(func):
        _eventBindings[event] = func
        return func
    return wrap

class WhatsappClient(cmd.Cmd):
    
    def __init__(self, configFile):
        cmd.Cmd.__init__(self)
        self.prompt = "@???:> "
        self.identchars += "/"
        readline.set_completer_delims(" ") 
    
        self.configFile = configFile
        self.config = readJSON(self.configFile)
        self._loadAliases()
        self.jid = "%s@s.whatsapp.net" % self.config["phone"]
        
        self.logfile = open(LOG_FILE, "a")
        
        connectionManager = YowsupConnectionManager()
        connectionManager.setAutoPong(True)
        self.cm = connectionManager
        self.signalsInterface = connectionManager.getSignalsInterface()
        self.methodsInterface = connectionManager.getMethodsInterface()
        for event, func in _eventBindings.iteritems():
            self.signalsInterface.registerListener(event, func.__get__(self))
        self.defaultReceiver = None
        self._login()
                
    def close(self):
        self.methodsInterface.call("presence_sendUnavailable")
        self.logfile.close()
        
    def _loadAliases(self):
        if os.path.exists(ALIASES_FILE):
            self.aliases = readJSON(ALIASES_FILE)
            self.aliasesRev = dict([(self.aliases[k], k) for k in self.aliases])
        else:
            self.aliases = {}
            self.aliasesRev = {}
    
    def _saveAliases(self):
        writeJSON(ALIASES_FILE, self.aliases)

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
        
    def parseline(self, line):
        if not line.startswith("/"):
            return (None, None, line)
        return cmd.Cmd.parseline(self, line[1:])
        
    def default(self, line):
        match = re.match("@([^:]*):[ ]*(.*)", line)
        if match:
            addr, msg = match.groups()
            self.do_send(addr, msg)
            return
        match = re.match("@([^:]*)", line)
        if match:
            addr = match.groups()[0]
            self.defaultReceiver = addr
            self.prompt = "@%s:> " % self.defaultReceiver
            return
        if line and self.defaultReceiver:
            msg = line.strip()
            self.do_send(self.defaultReceiver, msg)
            return
        print "Warning: line ignored (type /help to see a help message)"
        
    def postloop(self):
        print
        
    def do_EOF(self):
        return self.do_exit()
        
    def do_quit(self):
        return self.do_exit()

    def do_exit(self):
        self.close()
        return True
        
    def onecmd(self, line):
        cmd, args, line = self.parseline(line)
        if args:
            args = args.split()
        if line == "EOF":
            return self.do_EOF()
        if not line:
            return
        if not cmd:
            return self.default(line)
        if cmd == "help":
            return self.do_help(" ".join(args))
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            try:
                return func(*args)
            except Exception, exc:
                print exc
        
    def complete(self, text, nr):
        tokens = ["/%s" % c for c in self.completenames("")]
        tokens.remove("/EOF")
        for alias in self.aliases:
            tokens.append("@%s:" % alias)
            tokens.append(alias)
        matching = filter(lambda t: t.startswith(text), tokens)
        return matching[nr] if len(matching) >= nr else None
        
    def do_alias(self, *args):
        """
        Syntax: /alias alias=destination
        
        Assigns an alias to a destination.
        
        Instead of destination ids, the client can also use named aliases. If an alias exists for a
        destination id, it can be used instead of the destination id and it will be displayed on incoming
        messages.
        """
        alias, name = (" ".join(args)).split("=")
        print alias
        print name
        if name:
            self.aliases[alias] = name
            self.aliasesRev[name] = alias
        else:
            del self.aliasesRev[self.alias[alias]]
            del self.aliases[alias]
        self._saveAliases()

    def do_aliases(self):
        print ", ".join(["%s=%s" % (k, v) for k, v in self.aliases.iteritems()])
        
    def do_group_info(self, group):
        self.methodsInterface.call("group_getInfo", (self._name2jid(group),))

    @bind("group_gotInfo")
    def onGroupInfo(self, jid, owner, subject, subjectOwner, subjectTimestamp, creationTimestamp):
        creationTimestamp = datetime.datetime.fromtimestamp(creationTimestamp).strftime('%d-%m-%Y %H:%M')
        subjectTimestamp = datetime.datetime.fromtimestamp(subjectTimestamp).strftime('%d-%m-%Y %H:%M')
        self._out("Information on group %s: created by %s at %s, subject '%s' set by %s at %s" % (self._jid2name(jid), self._jid2name(owner), creationTimestamp, subject, self._jid2name(subjectOwner), subjectTimestamp))
            
    def do_group_invite(self, group, user):
        self.methodsInterface.call("group_addParticipant", (self._name2jid(group), self._name2jid(user)))
        
    def do_group_kick(self, group, user):
        self.methodsInterface.call("group_removeParticipant", (self._name2jid(group), self._name2jid(user)))
        
    def do_group_create(self, subject):
        self.methodsInterface.call("group_create", (subject,))
        
    @bind("group_createSuccess")
    def onGroupCreated(self, jid, groupJid):
        groupJid = "%s@%s" % (groupJid, jid) 
        self._out("New group: %s" % self._jid2name(groupJid))

    def do_group_destroy(self, group):
        self.methodsInterface.call("group_end", (self._name2jid(group),))
        
    @bind("group_endSuccess")
    def onGroupDestroyed(self, jid):
        pass #jid contains only "g.us" ????

    def do_group_subject(self, group, subject):
        self.methodsInterface.call("group_subject", (self._name2jid(group), subject))
        
    @bind("group_subjectReceived")
    def onGroupSubjectReceived(self, messageId, jid, author, subject, timestamp, wantsReceipt):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s changed subject of %s to '%s'" % (self._jid2name(author), self._jid2name(jid), subject), timestamp)
        if wantsReceipt:
            self.methodsInterface.call("subject_ack", (jid, messageId))

    def do_group_members(self, group):
        self.methodsInterface.call("group_getParticipants", (self._name2jid(group),))

    @bind("group_gotParticipants")
    def onGroupGotParticipants(self, groupJid, participants):
        self._out("Members of group %s: %s" % (self._jid2name(groupJid), [self._jid2name(p) for p in participants]))
                    
    def do_status(self, user):
        self.methodsInterface.call("presence_request", (self._name2jid(user),))
        
    @bind("presence_updated")
    def onPresenceUpdated(self, jid, lastseen):
        self._out("%s was last seen %s seconds ago" % (self._jid2name(jid), lastseen))
        
    @bind("notification_groupParticipantAdded")
    def onGroupParticipantAdded(self, groupJid, jid, author, timestamp, messageId, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s added %s to %s'" % (self._jid2name(author), self._jid2name(jid), self._jid2name(groupJid)), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))
    
    @bind("notification_groupParticipantRemoved")
    def onGroupParticipantRemoved(self, groupJid, jid, author, timestamp, messageId, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s removed %s from %s'" % (self._jid2name(author), self._jid2name(jid), self._jid2name(groupJid)), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))
        
    @bind("notification_contactProfilePictureUpdated")
    def onContactProfilePictureUpdated(self, jid, timestamp, messageId, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s updated his contact picture" % self._jid2name(jid), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("notification_groupPictureUpdated")
    def onGroupPictureUpdated(self, groupJid, author, timestamp, messageId, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s updated the picture for group %s" % (self._jid2name(author), self._jid2name(groupJid)), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))
            
    @bind("image_received")
    def onImageReceived(self, messageId, jid, preview, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends an image file (size: %d, url: %s)" % (self._jid2name(jid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("video_received")
    def onVideoReceived(self, messageId, jid, preview, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends a video file (size: %d, url: %s)" % (self._jid2name(jid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("audio_received")
    def onAudioReceived(self, messageId, jid, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends an audio file (size: %d, url: %s)" % (self._jid2name(jid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("location_received")
    def onLocationReceived(self, messageId, jid, name, preview, latitude, longitude, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends a location '%s' (lat: %f, long: %f)" % (self._jid2name(jid), name, latitude, longitude), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("vcard_received")
    def onVCardReceived(self, messageId, jid, name, data, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends contact information: %s" % (self._jid2name(jid), name), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (jid, messageId))

    @bind("group_imageReceived")
    def onGroupImageReceived(self, messageId, groupJid, author, preview, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends an image file to %s (size: %d, url: %s)" % (self._jid2name(author), self._jid2name(groupJid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))

    @bind("group_videoReceived")
    def onGroupVideoReceived(self, messageId, groupJid, author, preview, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends a video file to %s (size: %d, url: %s)" % (self._jid2name(author), self._jid2name(groupJid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))

    @bind("group_audioReceived")
    def onGroupAudioReceived(self, messageId, groupJid, author, url, size, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends an audio file to %s (size: %d, url: %s)" % (self._jid2name(author), self._jid2name(groupJid), size, url), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))

    @bind("group_locationReceived")
    def onGroupLocationReceived(self, messageId, groupJid, author, name, preview, latitude, longitude, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends a location to %s: '%s' (lat: %f, long: %f)" % (self._jid2name(author), self._jid2name(groupJid), name, latitude, longitude), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))

    @bind("group_vcardReceived")
    def onGroupVCardReceived(self, messageId, groupJid, author, name, data, receiptRequested):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s sends contact information to %s: %s" % (self._jid2name(author), self._jid2name(groupJid), name), timestamp)
        if receiptRequested:
            self.methodsInterface.call("notification_ack", (groupJid, messageId))

    def do_debug(self, debug):
        Debugger.enabled = debug.lower() in ["true", "1", "yes"]
        
    def do_send(self, receiver, msg):
        """
        Syntax: /send destination message
        
        Sends a message to a destination. There are two types of destinations:
        * Users can be addressed by their phone number (with country code and without any special 
          characters, e.g. 49179....)
        * Group chats can be addressed by prepending a # sign to the group chat id 
          (e.g. #491...-130...)
  
        Messages can also be sent to a destination by typing:
          @DESTINATION: MESSAGE
        A default destination ca be set by typing:
          @DESTINATION
        Any text that is neither an @DESTINATION nor a command will be sent to the default destination.
        """
        if not "@" in receiver:
           receiver = self._name2jid(receiver)
        self.methodsInterface.call("message_send", (receiver, msg))
        self._out("%s -> %s: %s" % (self._jid2name(self.jid), self._jid2name(receiver), msg), noOut=True)

    @bind("auth_success")
    def onAuthSuccess(self, username):
        self._out("Logged in as %s" % username)
        self.methodsInterface.call("ready")
        self.methodsInterface.call("presence_sendAvailable")

    @bind("auth_fail")
    def onAuthFailed(self, username, err):
        self._out("Auth Failed!")

    @bind("disconnected")
    def onDisconnected(self, reason):
        self._out("Disconnected because %s" %reason)
        try:
            self._login()
        except:
            pass

    def do_help(self, topic):
        if not topic:
            print GENERAL_DOC
        cmd.Cmd.do_help(self, topic)
            
    def _out(self, msg, timestamp=None, noOut=False):
        if not timestamp:
            timestamp = time.time()
        timestamp = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self.logfile.write("[%s] %s\n" % (timestamp, msg))
        self.logfile.flush()
        if not noOut:
            print "[%s] %s" % (timestamp, msg)
            
    @bind("message_received")
    def onMessageReceived(self, messageId, jid, messageContent, timestamp, wantsReceipt, pushName):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s: %s" % (self._jid2name(jid), messageContent), timestamp)
        if wantsReceipt:
            self.methodsInterface.call("message_ack", (jid, messageId))
            
    @bind("group_messageReceived")
    def onGroupMessageReceived(self, messageId, jid, author, messageContent, timestamp, wantsReceipt, pushName):
        formattedDate = datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')
        self._out("%s -> %s: %s" % (self._jid2name(author), self._jid2name(jid), messageContent), timestamp)
        if wantsReceipt:
            self.methodsInterface.call("message_ack", (jid, messageId))
            
    @bind("presence_available")
    def onPresenceAvailable(self, jid):
        self._out("%s is now available" % self._jid2name(jid))
        
    @bind("presence_unavailable")
    def onPresenceUnavailable(self, jid):
        self._out("%s is now unavailable" % self._jid2name(jid))


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
    writeJSON(CONFIG_FILE, config)
                     
if __name__ == "__main__":
    if not os.path.exists(CONFIG_PATH):
        os.mkdir(CONFIG_PATH)
    if not os.path.exists(CONFIG_FILE):
        configure(CONFIG_FILE)
    wa = WhatsappClient(CONFIG_FILE)
    print GENERAL_DOC
    try:
        wa.cmdloop()
    except:
        import traceback
        traceback.print_exc()
        wa.close()
