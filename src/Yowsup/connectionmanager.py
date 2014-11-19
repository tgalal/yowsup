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

from Yowsup.ConnectionIO.protocoltreenode import ProtocolTreeNode
from Yowsup.ConnectionIO.ioexceptions import ConnectionClosedException
from Yowsup.ConnectionIO.connectionengine import ConnectionEngine
from Yowsup.Common.utilities import Utilities

from Yowsup.Common.debugger import Debugger
import threading, select, time
from Yowsup.Common.watime import WATime
from .Auth.auth import YowsupAuth
from Yowsup.Common.constants import Constants
from Yowsup.Interfaces.Lib.LibInterface import LibMethodInterface, LibSignalInterface
import tempfile
from random import randrange
import socket
import hashlib
import base64
import sys


import traceback
class YowsupConnectionManager:
	
	def __init__(self):
		Debugger.attach(self)
		self.currKeyId = 0
		self.iqId = 0
		self.verbose = True
		self.state = 0
		self.lock = threading.Lock()
		self.autoPong = True
		
		self.domain = "s.whatsapp.net"
	
		#self.methodInterface = MethodInterface(authenticatedSocketConnection.getId())
		#self.signalInterface = SignalInterface(authenticatedSocketConnection.getId())
		self.readerThread = None
		
		self.methodInterface = LibMethodInterface()
		self.signalInterface = LibSignalInterface()
		self.readerThread = ReaderThread()
		self.readerThread.setSignalInterface(self.signalInterface)
		

		self.bindMethods()
	
	
	def setInterfaces(self, signalInterface, methodInterface):
		self.methodInterface = methodInterface
		self.signalInterface = signalInterface
		
		self.readerThread.setSignalInterface(self.signalInterface)
		
		self.bindMethods()
		
	def getSignalsInterface(self):
		return self.signalInterface
	
	def getMethodsInterface(self):
		return self.methodInterface

	def setAutoPong(self, autoPong):
		self.autoPong = self.readerThread.autoPong = autoPong
	
	def startReader(self):
		if self.readerThread.isAlive():
			self._d("Reader already started")
			return 0

		self._d("starting reader")
		try:
			self.readerThread.start()
			self._d("started")
		except RuntimeError:
			self._d("Reader already started before")
			self.readerThread.sendDisconnected()
			return 0
		
		return 1
	
	
	def block(self):
		self.readerThread.join()

	def bindMethods(self):
		self.methodInterface.registerCallback("getVersion", lambda: Constants.v)
		self.methodInterface.registerCallback("message_send",self.sendText)
		self.methodInterface.registerCallback("message_imageSend",self.sendImage)
		self.methodInterface.registerCallback("message_audioSend",self.sendAudio)
		self.methodInterface.registerCallback("message_videoSend",self.sendVideo)
		self.methodInterface.registerCallback("message_locationSend",self.sendLocation)
		self.methodInterface.registerCallback("message_vcardSend",self.sendVCard)
		
		self.methodInterface.registerCallback("message_broadcast",self.sendBroadcast)

		self.methodInterface.registerCallback("message_ack",self.sendMessageReceipt)

		self.methodInterface.registerCallback("notification_ack", self.sendNotificationReceipt)
		
		self.methodInterface.registerCallback("clientconfig_send",self.sendClientConfig)

		self.methodInterface.registerCallback("delivered_ack",self.sendDeliveredReceiptAck)

		self.methodInterface.registerCallback("visible_ack",self.sendVisibleReceiptAck)

		self.methodInterface.registerCallback("typing_send",self.sendTyping)
		self.methodInterface.registerCallback("typing_paused",self.sendPaused)

		self.methodInterface.registerCallback("group_getGroups", self.sendGetGroups)
		self.methodInterface.registerCallback("group_getInfo",self.sendGetGroupInfo)
		self.methodInterface.registerCallback("group_create",self.sendCreateGroupChat)
		self.methodInterface.registerCallback("group_addParticipants",self.sendAddParticipants)
		self.methodInterface.registerCallback("group_removeParticipants",self.sendRemoveParticipants)
		self.methodInterface.registerCallback("group_leave",self.sendLeaveGroupChat)
		self.methodInterface.registerCallback("group_delete",self.sendDeleteGroupChat)
		self.methodInterface.registerCallback("group_setSubject",self.sendSetGroupSubject)
		self.methodInterface.registerCallback("group_setPicture", self.sendSetPicture)
		self.methodInterface.registerCallback("group_getPicture", self.sendGetPicture)
		
		self.methodInterface.registerCallback("group_getParticipants",self.sendGetParticipants)

		self.methodInterface.registerCallback("picture_get",self.sendGetPicture)
		self.methodInterface.registerCallback("picture_getIds",self.sendGetPictureIds)

		self.methodInterface.registerCallback("contact_getProfilePicture", self.sendGetPicture)

		self.methodInterface.registerCallback("status_update",self.sendChangeStatus)

		self.methodInterface.registerCallback("presence_request",self.getLastOnline)
		self.methodInterface.registerCallback("presence_unsubscribe",self.sendUnsubscribe)
		self.methodInterface.registerCallback("presence_subscribe",self.sendSubscribe)
		self.methodInterface.registerCallback("presence_sendAvailableForChat",self.sendAvailableForChat)
		self.methodInterface.registerCallback("presence_sendAvailable",self.sendAvailable)
		self.methodInterface.registerCallback("presence_sendUnavailable",self.sendUnavailable)
		
		
		self.methodInterface.registerCallback("profile_setPicture", self.sendSetProfilePicture)
		self.methodInterface.registerCallback("profile_getPicture", self.sendGetProfilePicture)
		
		self.methodInterface.registerCallback("profile_setStatus", self.sendChangeStatus)

		self.methodInterface.registerCallback("sync_sendSync", self.sendSync)
		
		self.methodInterface.registerCallback("disconnect", self.disconnect)
		self.methodInterface.registerCallback("ready", self.startReader)
		
		self.methodInterface.registerCallback("auth_login", self.auth)
		
		self.methodInterface.registerCallback("media_requestUpload", self.sendRequestUpload)
		
		self.methodInterface.registerCallback("sync_sendContacts", self.sendSyncContacts)
		self.methodInterface.registerCallback("sync_getStatuses", self.sendGetStatuses)

		self.methodInterface.registerCallback("privacy_setList", self.sendSetPrivacyList)
		self.methodInterface.registerCallback("privacy_getList", self.sendGetPrivacyList)

		self.methodInterface.registerCallback("privacy_setSettings", self.sendSetPrivacySettings)
		self.methodInterface.registerCallback("privacy_getSettings", self.sendGetPrivacySettings)

		self.methodInterface.registerCallback("account_delete", self.sendAccountDelete)

		self.methodInterface.registerCallback("subscription_generateLink", self.generateSubscriptionLink)


	def disconnect(self, reason=""):
		self._d("Disconnect sequence initiated")
		self._d("Sending term signal to reader thread")
		if self.readerThread.isAlive():
			self.readerThread.terminate()
			self._d("Shutting down socket")
			self.socket.close()
			self._d("Waiting for readerThread to die")
			self.readerThread.join()
		self._d("Disconnected!")
		self._d(reason)
		self.state = 0
		self.readerThread.sendDisconnected(reason)


	def getConnection(self):
		return self.socket

	def triggerEvent(self, eventName, stanza):
		if eventName in self.events and self.events[eventName] is not None:
			self.events[eventName](stanza)

	def bindEvent(self, eventName, callback):
		if eventName in self.events:
			self.events[eventName] = callback

	##########################################################

	def _writeNode(self, node):
		if self.state == 2:
			try:
				self.out.write(node)
				return True
			except ConnectionClosedException:
				self._d("CONNECTION DOWN")
				#self.disconnect("closed")
				if self.readerThread.isAlive():
					self.readerThread.terminate()
					self.readerThread.join()
					self.readerThread.sendDisconnected("closed")
		
		return False
		
	def onDisconnected(self):
		self._d("Setting state to 0")
		self.state = 0

	def auth(self, username, password):
		self._d(">>>>>>>>                         AUTH CALLED")
		username = str(username)
		#password = str(password)
		#traceback.print_stack()
		
		self.lock.acquire()
		if self.state == 0 :
		
			
			if self.readerThread.isAlive():
				raise Exception("TWO READER THREADS ON BOARD!!")
			
			self.readerThread = ReaderThread()
			self.readerThread.autoPong = self.autoPong
			self.readerThread.setSignalInterface(self.signalInterface)
			yAuth = YowsupAuth(ConnectionEngine())
			try:
				self.state = 1
				tokenData = Utilities.readToken()
				resource = tokenData["r"] if tokenData else Constants.tokenData["r"]
				connection = yAuth.authenticate(username, password, Constants.domain, resource)
			except socket.gaierror:
				self._d("DNS ERROR")
				self.readerThread.sendDisconnected("dns")
				#self.signalInterface.send("disconnected", ("dns",))
				self.lock.release()
				self.state = 0
				
				return 0
			except socket.error:
				self._d("Socket error, connection timed out")
				self.readerThread.sendDisconnected("closed")
				#self.signalInterface.send("disconnected", ("closed",))
				self.lock.release()
				self.state = 0
				
				return 0
			except ConnectionClosedException:
				self._d("Conn closed Exception")
				self.readerThread.sendDisconnected("closed")
				#self.signalInterface.send("disconnected", ("closed",))
				self.lock.release()
				self.state = 0
				
				return 0
		
			if not connection:
				self.state = 0
				self.signalInterface.send("auth_fail", (username, "invalid"))
				self.lock.release()
				return 0
			
			self.state = 2
			
			
	
			self.socket = connection
			self.jid = self.socket.jid
			#@@TODO REPLACE PROPERLY
			self.out = self.socket.writer
			
			self.readerThread.setSocket(self.socket)
			self.readerThread.disconnectedCallback = self.onDisconnected
			self.readerThread.sendReceiptAck = self.sendReceiptAck
			self.readerThread.onPing = self.sendPong
			self.readerThread.ping = self.sendPing
			self.readerThread.sendNotificationReceived = self.sendNotificationReceived
			
	
			self.signalInterface.send("auth_success", (username,))
		self.lock.release()
			
		
		
		
	def sendTyping(self,jid):
		self._d("SEND TYPING TO JID")
		composing = ProtocolTreeNode("composing")
		message = ProtocolTreeNode("chatstate",{"to":jid},[composing]);
		self._writeNode(message);



	def sendPaused(self,jid):
		self._d("SEND PAUSED TO JID")
		composing = ProtocolTreeNode("paused")
		message = ProtocolTreeNode("chatstate",{"to":jid},[composing]);
		self._writeNode(message);


	def sendMessageReceipt(self, jid, msgId):
		self.sendReceipt(jid, "chat", msgId)

	def sendNotificationReceipt(self, jid, notificationId):
		self.sendReceipt(jid, "notification", notificationId)

	def sendReceipt(self,jid,mtype,mid):
		self._d("sending message received to "+jid+" - type:"+mtype+" - id:"+mid)
		attr = {"to": jid, "id": mid}
		if mtype == "read":
		  attr["type"] = "read"
		receiptNode = ProtocolTreeNode("receipt", attr)
		self._writeNode(receiptNode)


	def sendDeliveredReceiptAck(self,to,msg_id):
		self._writeNode(self.getReceiptAck(to,msg_id,"delivered"));

	def sendVisibleReceiptAck(self,to,msg_id):
		self._writeNode(self.getReceiptAck(to,msg_id,"visible"));

	def getReceiptAck(self,to,msg_id,receiptType):
		ackNode = ProtocolTreeNode("ack",{"xmlns":"urn:xmpp:receipts","type":receiptType})
		messageNode = ProtocolTreeNode("message",{"to":to,"type":"chat","id":msg_id},[ackNode]);
		return messageNode;

	def sendReceiptAck(self, msg_id, receiptType):
		ackNode = ProtocolTreeNode("ack",{"class": "receipt", "type": "delivery" if receiptType is None else receiptType, "id": msg_id})
		self._writeNode(ackNode);

	def sendMessageReceived(self, jid, msg_id):
		receiptNode = ProtocolTreeNode("receipt",{"to": jid, "id": msg_id})
		self._writeNode(receiptNode)

	def sendNotificationReceived(self, to, msg_id, from_jid, participant, notificationType, childNode):
		attrs = {"to": to, "class": "notification", "id": msg_id, "type": notificationType}
		if participant is not None:
			attrs["participant"] = participant
		if from_jid is not None:
			attrs["from"] = from_jid
		ackNode = ProtocolTreeNode("ack", attrs, [childNode] if childNode is not None else None)
		self._writeNode(ackNode)

	def sendCleanDirty(self, dirtyType):
		idx = self.makeId("clean_dirty_")
		cleanNode = ProtocolTreeNode("clean", {"type": dirtyType})
		iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "set", "to": self.domain, "xmlns": "urn:xmpp:whatsapp:dirty"}, [cleanNode])
		self._writeNode(iqNode);

	def makeId(self,prefix):
		self.iqId += 1
		idx = ""
		if self.verbose:
			idx += prefix + str(self.iqId);
		else:
			idx = "%x" % self.iqId

		return idx

	def sendPing(self):

		idx = self.makeId("ping_")

		self.readerThread.requests[idx] = self.readerThread.parsePingResponse;

		pingNode = ProtocolTreeNode("ping");
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":self.domain,"xmlns":"w:p"},[pingNode]);
		self._writeNode(iqNode);
		return idx


	def sendPong(self,idx):
		iqNode = ProtocolTreeNode("iq",{"type":"result","to":self.domain,"id":idx})
		self._writeNode(iqNode);

	def getLastOnline(self,jid):

		if len(jid.split('-')) == 2 or jid == "Server@s.whatsapp.net": #SUPER CANCEL SUBSCRIBE TO GROUP AND SERVER
			return

		self.sendSubscribe(jid);

		self._d("presence request Initiated for %s"%(jid))
		idx = self.makeId("last_")
		self.readerThread.requests[idx] = self.readerThread.parseLastOnline;

		query = ProtocolTreeNode("query");
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":jid,"xmlns":"jabber:iq:last"},[query]);
		self._writeNode(iqNode)


	def sendIq(self):
		node = ProtocolTreeNode("iq",{"to":"g.us","type":"get","id":str(int(time.time()))+"-0"},None,'expired');
		self._writeNode(node);

		node = ProtocolTreeNode("iq",{"to":"s.whatsapp.net","type":"set","id":str(int(time.time()))+"-1"},None,'expired');
		self._writeNode(node);

	def sendAvailableForChat(self, pushname):
		presenceNode = ProtocolTreeNode("presence",{"name":pushname})
		self._writeNode(presenceNode);

	def sendAvailable(self):
		presenceNode = ProtocolTreeNode("presence",{"type":"available"})
		self._writeNode(presenceNode);


	def sendUnavailable(self):
		presenceNode = ProtocolTreeNode("presence",{"type":"unavailable"})
		self._writeNode(presenceNode);


	def sendSubscribe(self,to):
		presenceNode = ProtocolTreeNode("presence",{"type":"subscribe","to":to});

		self._writeNode(presenceNode);


	def sendUnsubscribe(self,to):
		presenceNode = ProtocolTreeNode("presence",{"type":"unsubscribe","to":to});

		self._writeNode(presenceNode);


	def mediaNode(fn):
		def wrapped(self, *args):
				mediaType = fn(self, *args)
				
				
				url = args[1]
				name = args[2]
				size = args[3]
				
				mmNode = ProtocolTreeNode("media", {"type":mediaType,"file":name,"size":size,"url":url},None, args[4:][0] if args[4:] else None);
				return mmNode
			
		return wrapped
	
	def sendMessage(fn):
			def wrapped(self, *args):
				node = fn(self, *args)
				jid = "broadcast" if type(args[0]) == list else args[0]
				messageNode = self.getMessageNode(jid, node)
				
				self._writeNode(messageNode);

				return messageNode.getAttributeValue("id")
			
			return wrapped
		
	def sendChangeStatus(self,status):
		self._d("updating status to: %s"%(status))

		idx = self.makeId("send_status_")
		statusNode = ProtocolTreeNode("status", None, None, status)
		iqNode = ProtocolTreeNode("iq", {"to": self.domain, "type": "set", "id": idx, "xmlns": "status"}, [statusNode]);
		
		self._writeNode(iqNode);
		
		return messageNode.getAttributeValue("id")
		
		
	
	@sendMessage
	def sendText(self,jid, content):
		return ProtocolTreeNode("body",None,None,content);

	@sendMessage
	@mediaNode
	def sendImage(self, jid, url, name, size, preview):
		return "image"
	
	@sendMessage
	@mediaNode
	def sendVideo(self, jid, url, name, size, preview):
		return "video"
	
	@sendMessage
	@mediaNode
	def sendAudio(self, jid, url, name, size):
		return "audio"

	@sendMessage
	def sendLocation(self, jid, latitude, longitude, preview):
		self._d("sending location (" + latitude + ":" + longitude + ")")

		return ProtocolTreeNode("media", {"type":"location","latitude":latitude,"longitude":longitude},None,preview)
		
	@sendMessage
	def sendVCard(self, jid, data, name):
		
		cardNode = ProtocolTreeNode("vcard",{"name":name},None,data);
		return ProtocolTreeNode("media", {"type":"vcard"},[cardNode])
	
	@sendMessage
	def sendBroadcast(self, jids, content):
		
		broadcastNode = ProtocolTreeNode("broadcast", None, [ProtocolTreeNode("to", {"jid": jid}) for jid in jids])
		
		messageNode = ProtocolTreeNode("body",None,None,content);
		
		return [broadcastNode, messageNode]

	def sendClientConfig(self):
		idx = self.makeId("config_");
		configNode = ProtocolTreeNode("config",{"platform":"none"})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":self.domain,"xmlns":"urn:xmpp:whatsapp:push"},[configNode]);
		self.readerThread.requests[idx] = self.readerThread.parseResultNode;

		self._writeNode(iqNode);


	# gtype should be either "participating" or "owning"
	def sendGetGroups(self,gtype):
		self._d("getting groups %s"%(gtype))
		idx = self.makeId("get_groups_")
		self.readerThread.requests[idx] = self.readerThread.parseGroups;

		queryNode = ProtocolTreeNode("list",{"type":gtype})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":"g.us","xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendGetGroupInfo(self,jid):
		self._d("getting group info for %s"%(jid))
		idx = self.makeId("get_g_info_")
		self.readerThread.requests[idx] = self.readerThread.parseGroupInfo;

		queryNode = ProtocolTreeNode("query")
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":jid,"xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendCreateGroupChat(self,subject):
		self._d("creating group: %s"%(subject))
		idx = self.makeId("create_group_")
		self.readerThread.requests[idx] = self.readerThread.parseGroupCreated;

		queryNode = ProtocolTreeNode("group",{"action":"create","subject":subject})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":"g.us","xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendDeleteGroupChat(self,gjid):
		self._d("creating group: %s"%(subject))
		idx = self.makeId("create_group_")
		self.readerThread.requests[idx] = self.readerThread.parseGroupCreated;

		queryNode = ProtocolTreeNode("group",{"action":"delete"})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":gjid,"xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendAddParticipants(self, gjid, participants):
		self._d("opening group: %s"%(gjid))
		self._d("adding participants: %s"%(participants))
		idx = self.makeId("add_group_participants_")
		self.readerThread.requests[idx] = self.readerThread.parseAddedParticipants;
		
		innerNodeChildren = []

		for part in participants:
			innerNodeChildren.append( ProtocolTreeNode("participant",{"jid":part}) )

		queryNode = ProtocolTreeNode("add",None,innerNodeChildren)
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":gjid,"xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendRemoveParticipants(self,gjid, participants):
		self._d("opening group: %s"%(gjid))
		self._d("removing participants: %s"%(participants))
		idx = self.makeId("remove_group_participants_")
		self.readerThread.requests[idx] = self.readerThread.parseRemovedParticipants;

		innerNodeChildren = []
		for part in participants:
			innerNodeChildren.append( ProtocolTreeNode("participant",{"jid":part}) )

		queryNode = ProtocolTreeNode("remove",None,innerNodeChildren)
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":gjid,"xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)


	def sendLeaveGroupChat(self,gjid):
		self._d("removing group: %s"%(gjid))
		idx = self.makeId("leave_group_")
		self.readerThread.requests[idx] = self.readerThread.parseGroupEnded;

		innerNodeChildren = []
		innerNodeChildren.append( ProtocolTreeNode("group",{"id":gjid}) )

		queryNode = ProtocolTreeNode("leave",None,innerNodeChildren)
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":"g.us","xmlns":"w:g"},[queryNode])

		self._writeNode(iqNode)

	def sendSetGroupSubject(self,gjid,subject):
		#subject = subject.encode('utf-8')
		#self._d("setting group subject of " + gjid + " to " + subject)
		idx = self.makeId("set_group_subject_")
		self.readerThread.requests[idx] = self.readerThread.parseGroupSubject

		queryNode = ProtocolTreeNode("subject",{"value":subject})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"set","to":gjid,"xmlns":"w:g"},[queryNode]);

		self._writeNode(iqNode)


	def sendGetParticipants(self,jid):
		idx = self.makeId("get_participants_")
		self.readerThread.requests[idx] = self.readerThread.parseParticipants

		listNode = ProtocolTreeNode("list")
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":jid,"xmlns":"w:g"},[listNode]);

		self._writeNode(iqNode)


	def sendGetPicture(self,jid):
		self._d("GETTING PICTURE FROM " + jid)
		idx = self.makeId("get_picture_")

		#@@TODO, ?!
		self.readerThread.requests[idx] =  self.readerThread.parseGetPicture

		listNode = ProtocolTreeNode("picture",{"type":"image"})
		iqNode = ProtocolTreeNode("iq",{"id":idx,"to":jid,"type":"get","xmlns":"w:profile:picture"},[listNode]);

		self._writeNode(iqNode)



	def sendGetPictureIds(self,jids):
		idx = self.makeId("get_picture_ids_")
		self.readerThread.requests[idx] = self.readerThread.parseGetPictureIds

		innerNodeChildren = []
		for jid in jids:
			innerNodeChildren.append( ProtocolTreeNode("user",{"jid": jid}) )

		queryNode = ProtocolTreeNode("list",None,innerNodeChildren)
		iqNode = ProtocolTreeNode("iq",{"id":idx,"type":"get","to":self.jid,"xmlns":"w:profile:picture"},[queryNode])

		self._writeNode(iqNode)

	
	def sendGetProfilePicture(self):
		return self.sendGetPicture(self.jid)
	
	def sendSetProfilePicture(self, filepath):
		return self.sendSetPicture(self.jid, filepath)
	
	def sendSetPicture(self, jid, imagePath):

		f = open(imagePath, 'rb')
		imageData = f.read()
		imageData = bytearray(imageData)
		f.close()
		
		idx = self.makeId("set_picture_")
		self.readerThread.requests[idx] = self.readerThread.parseSetPicture

		listNode = ProtocolTreeNode("picture",{"type":"image"}, None, imageData)

		iqNode = ProtocolTreeNode("iq",{"id":idx,"to":jid,"type":"set","xmlns":"w:profile:picture"},[listNode])

		self._writeNode(iqNode)

	
	def sendRequestUpload(self, b64Hash, t, size, b64OrigHash = None):
		idx = self.makeId("upload_")
		
		self.readerThread.requests[idx] = lambda iqresnode: self.readerThread.parseRequestUpload(iqresnode, b64Hash)

		if type(size) is not str:
			size = str(size)

		attribs = {"hash":b64Hash, "type":t, "size":size}

		if b64OrigHash:
			attribs["orighash"] = b64OrigHash

		mediaNode = ProtocolTreeNode("media", attribs)
		iqNode = ProtocolTreeNode("iq",{"id":idx,"to":"s.whatsapp.net","type":"set","xmlns":"w:m"},[mediaNode])
		
		
		self._writeNode(iqNode)


	def sendSync(self, contacts):
		idx = self.makeId("sendsync_")
		self.readerThread.requests[idx] = self.readerThread.parseSync
		
		users = []
		
		for c in contacts:
			users.append(ProtocolTreeNode("user",None,None,'+' + c.replace('+', '')))

		node = ProtocolTreeNode(
			"iq", 
			{
				"type" : "get",
				"id" : idx,
				"xmlns" : "urn:xmpp:whatsapp:sync"
			}, 
			[
				(
				ProtocolTreeNode(
				"sync", 
				{
					"mode" : 'full',
					"context" : 'registration',
					"sid" : str((time.time() + 11644477200) * 10000000),
					"index" : '0',
					"last" : "true",
				}, 
				users, 
				None)
			  ),
		]
		, None)
		self._writeNode(node)


	def getMessageNode(self, jid, child):
			serverNode = ProtocolTreeNode("server",None);
			xNode = ProtocolTreeNode("x",{"xmlns":"jabber:x:event"},[serverNode]);
			messageChildren = []
			
			if type(child) == list:
				messageChildren = child
			else:
				messageChildren.append(child)
			messageChildren.append(xNode)
				
			msgId = str(int(time.time()))+"-"+ str(self.currKeyId)
			
			messageNode = ProtocolTreeNode("message",{"to":jid,"type":"text","id":msgId},messageChildren)
			
			self.currKeyId += 1


			return messageNode;

	def sendSyncContacts(self, numbers):
		print("sendSyncContacts")
		syncNodes = []
		for number in numbers:
			print(number)
			if number.find("@") >= 0:
				number = "+" + number.split("@")[0]
			userNode = ProtocolTreeNode("user", None, None, number)
			syncNodes.append(userNode)
		if len(syncNodes) > 0:
			idx = self.makeId("sync_")
			self.readerThread.requests[idx] = self.readerThread.parseSyncContacts
			syncNode = ProtocolTreeNode("sync", {"context": "background", "index": 0, "mode": "delta", "last": "true", "sid": str(int(time.time()))}, syncNodes)
			iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "get", "to": self.jid, "xmlns": "urn:xmpp:whatsapp:sync"}, syncNode)
			self._writeNode(iqNode)

	def sendGetStatuses(self, jids):
		syncNodes = []
		for cjid in cjids:
			userNode = ProtocolTreeNode("user", {"jid": cjid})
			syncNodes.append(userNode)
		if len(syncNodes) > 0:
			idx = self.makeId("sync_statuses_")
			self.readerThread.requests[idx] = self.readerThread.parseSyncStatuses
			statusNode = ProtocolTreeNode("status", None, syncNodes)
			iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "get", "to": self.domain, "xmlns": "status"}, statusNode)
			self._writeNode(iqNode)

	def sendSetPrivacyList(self, cjids):
		privacyNodes = []
		order = 0
		for cjid in cjids:
			itemNode = ProtocolTreeNode("item", {"type": "jid", "value": cjid, "action": "deny", "order": order})
			order += 1
		if len(privacyNodes) > 0:
			idx = self.makeId("privacy_setlist_")
			listNode = ProtocolTreeNode("list", {"name": "default"}, privacyNodes)
			queryNode = ProtocolTreeNode("query", None, [listNode])
			iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "set", "xmlns": "jabber:iq:privacy"}, [queryNode])
			self._writeNode(iqNode)

	def sendGetPrivacyList(self):
		idx = self.makeId("privacy_getlist_")
		self.readerThread.requests[idx] = self.readerThread.parsePrivacyList
		listNode = ProtocolTreeNode("list", {"name": "default"})
		queryNode = ProtocolTreeNode("query", {}, [listNode])
		iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "get", "xmlns": "jabber:iq:privacy"}, [queryNode])
		self._writeNode(iqNode)

	def sendSetPrivacySettings(self, key, value):
		idx = self.makeId("privacy_setvalue_")
		categoryNode = ProtocolTreeNode("category", {"name": key, "value": value})
		privacyNode = ProtocolTreeNode("privacy", None, [categoryNode])
		iqNode = ProtocolTreeNode("iq", {"id": idx, "to": self.domain, "type": "set", "xmlns": "privacy"}, [privacyNode])
		self._writeNode(iqNode)

	def sendGetPrivacySettings(self):
		idx = self.makeId("privacy_getvalues_")
		self.readerThread.requests[idx] = self.readerThread.parsePrivacySettings
		privacyNode = ProtocolTreeNode("privacy")
		iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "get", "to": self.domain, "xmlns": "privacy"}, [privacyNode])
		self._writeNode(iqNode)

	def sendAccountDelete(self):
		idx = self.makeId("account_delete_")
		self.readerThread.requests[idx] = self.readerThread.parseAccountDelete
		removeNode = ProtocolTreeNode("remove")
		iqNode = ProtocolTreeNode("iq", {"id": idx, "type": "get", "to": self.domain, "xmlns": "urn:xmpp:whatsapp:account"}, [removeNode])
		self._writeNode(iqNode)

	def generateSubscriptionLink(self, mode, years):
		phone = self.jid.split("@")[0]
		chksum = hashlib.md5(phone + "abc").hexdigest()
		link = "https://www.whatsapp.com/payments/" + mode + ".php?phone=" + phone + "&cksum=" + chksum + "&sku=" + years
		self.signalInterface.send("subscription_link", (link, ))


class ReaderThread(threading.Thread):
	def __init__(self):
		Debugger.attach(self);

		self.signalInterface = None
		#self.socket = connection
		self.terminateRequested = False
		self.disconnectedSent = False
		self.timeout = 180
		self.selectTimeout = 3
		self.requests = {};
		self.lock = threading.Lock()
		self.disconnectedCallback = None
		self.autoPong = True
		self.onPing = self.ping = None

		super(ReaderThread,self).__init__();

		self.daemon = True
	def setSocket(self, connection):
		self.socket = connection

	def setSignalInterface(self, signalInterface):
		self.signalInterface = signalInterface

	def terminate(self):
		self._d("attempting to exit gracefully")
		self.terminateRequested = True
		

	def sendDisconnected(self, reason="noreason"):
		self._d("Sending disconnected because of %s" % reason)
		self.lock.acquire()
		if not self.disconnectedSent:
			self.disconnectedSent = True
			if self.disconnectedCallback:
				self.disconnectedCallback()
			self.lock.release()
			self.signalInterface.send("disconnected", (reason,))

	def run(self):
		self._d("Read thread startedX");
		while True:
			try:
				ready = select.select([self.socket.reader.rawIn], [], [], self.selectTimeout)
			except:
				self._d("Error in ready")
				raise
				return
			
			if self.terminateRequested:
				return

			if ready[0]:
				try:
					node = self.socket.reader.nextTree()
				except ConnectionClosedException:
					#print traceback.format_exc()
					self._d("Socket closed, got 0 bytes!")
					#self.signalInterface.send("disconnected", ("closed",))
					self.sendDisconnected("closed")
					return

				if node is not None:
					if ProtocolTreeNode.tagEquals(node, "stream:error"):
						childNode = node.getChild(0)
						reason = childNode.getAttributeValue("text")
						self._d("Stream error!")
						self.sendDisconnected("stream:error" if reason is None else reason)

					elif ProtocolTreeNode.tagEquals(node,"iq"):
						iqType = node.getAttributeValue("type")
						idx = node.getAttributeValue("id")
						iqxmlns = node.getAttributeValue("xmlns")

						if iqType is None:
							raise Exception("iq doesn't have type")

						if iqxmlns == "urn:xmpp:ping":
							self.onPing(idx)
						elif iqType == "result":
							if idx in self.requests:
								self.requests[idx](node)
								del self.requests[idx]
							else:
								self._d("unexpected result id: " + idx)

						elif iqType == "error":
							if idx in self.requests:
								self.requests[idx](node)
								del self.requests[idx]
						elif iqType == "get":
							childNode = node.getChild(0)
							
							if ProtocolTreeNode.tagEquals(childNode,"query") and node.getAttributeValue("from") is not None and "http://jabber.org/protocol/disco#info" == childNode.getAttributeValue("xmlns"):
								pin = childNode.getAttributeValue("pin");
								timeoutString = childNode.getAttributeValue("timeout");
								try:
									timeoutSeconds = int(timeoutString) if timeoutString is not None else None
								except ValueError:
									raise Exception("relay-iq exception parsing timeout %s "%(timeoutString))

								if pin is not None:
									self.eventHandler.onRelayRequest(pin,timeoutSeconds,idx)
						elif iqType == "set":
							childNode = node.getChild(0)
							if ProtocolTreeNode.tagEquals(childNode,"query"):
								xmlns = childNode.getAttributeValue("xmlns")

								if xmlns == "jabber:iq:roster":
									itemNodes = childNode.getAllChildren("item");
									ask = ""
									for itemNode in itemNodes:
										jid = itemNode.getAttributeValue("jid")
										subscription = itemNode.getAttributeValue("subscription")
										ask = itemNode.getAttributeValue("ask")
						else:
							raise Exception("Unkown iq type %s"%(iqType))

					elif ProtocolTreeNode.tagEquals(node, "ib"):
						dirtyNode = node.getChild("dirty")
						if dirtyNode is not None:
							dirtyType = dirtyNode.getAttributeValue("type")
							self.signalInterface.send("ib_dirty", (dirtyType,))
                            ##sendCleanDirty(dirtyType)

					elif ProtocolTreeNode.tagEquals(node,"presence"):
						jid = node.getAttributeValue("from")

						if jid is not None:
							presenceType = node.getAttributeValue("type")
							if presenceType == "unavailable":
								self.signalInterface.send("presence_unavailable", (jid,))
							elif presenceType is None or presenceType == "available":
								self.signalInterface.send("presence_available", (jid,))

					elif ProtocolTreeNode.tagEquals(node, "notification"):

						receiptRequested = True;
						notificationType = None

						notificationType = node.getAttributeValue("type");
						notificationId = node.getAttributeValue("id");
						notificationTo = node.getAttributeValue("to");
						fromJid = node.getAttributeValue("from");
						timestamp =int(node.getAttributeValue("t"))
						msgId = node.getAttributeValue("id")
							
						if notificationType == "picture":
							bodyNode = node.getChild("set")
							
							if bodyNode:
								pictureId = int(bodyNode.getAttributeValue("id"))
								if "-" in bodyNode.getAttributeValue("jid"):
									self.signalInterface.send("notification_groupPictureUpdated",(bodyNode.getAttributeValue("jid"), bodyNode.getAttributeValue("author"), timestamp, msgId, pictureId, receiptRequested))
								else:
									self.signalInterface.send("notification_contactProfilePictureUpdated",(bodyNode.getAttributeValue("jid"), timestamp, msgId, pictureId, receiptRequested))

							else:
								bodyNode = notifNode.getChild("delete")

								if bodyNode:
									if "-" in bodyNode.getAttributeValue("jid"):
										self.signalInterface.send("notification_groupPictureRemoved",(bodyNode.getAttributeValue("jid"), bodyNode.getAttributeValue("author"), timestamp, msgId, receiptRequested))
									else:
										self.signalInterface.send("notification_contactProfilePictureRemoved",(bodyNode.getAttributeValue("jid"), timestamp, msgId, receiptRequested))

							#if isGroup:
							#	
							#	self.signalInterface.send("notification_groupPictureUpdated",(bodyNode.getAttributeValue("jid"), bodyNode.getAttributeValue("author"), timestamp, msgId, receiptRequested))
							#else:
							#	self.signalInterface.send("notification_contactProfilePictureUpdated",(bodyNode.getAttributeValue("jid"), timestamp, msgId, receiptRequested))

							#self.sendNotificationReceived(notificationTo, notificationId, fromJid, participant, notificationType, None)

						elif notificationType == "participant":
							addSubject = None
							removeSubject = None
							author = None

							bodyNode = node.getChild("add");
							if bodyNode is not None:
								addSubject = bodyNode.getAttributeValue("jid");
								author = bodyNode.getAttributeValue("author") or addSubject

							bodyNode = node.getChild("remove");
							if bodyNode is not None:
								removeSubject = bodyNode.getAttributeValue("jid");
								author = bodyNode.getAttributeValue("author") or removeSubject

							if addSubject is not None:
								
								self.signalInterface.send("notification_groupParticipantAdded", (fromAttribute, addSubject, author, timestamp, msgId, receiptRequested))
								
							if removeSubject is not None:
								self.signalInterface.send("notification_groupParticipantRemoved", (fromAttribute, removeSubject, author, timestamp, msgId, receiptRequested))

							#self.sendNotificationReceived(notificationTo, notificationId, fromJid, participant, notificationType, None)

						elif notificationType == "web":
							self._d("web notification not implemented")

							#self.sendNotificationReceived(fromJid, notificationId, notificationTo, participant, notificationType, None)

						elif notificationType == "status":
							setNode = node.getChild("set")
							status = None if setNode is None else (setNode.data if sys.version_info < (3, 0) else setNode.data.encode('latin-1').decode());
							
							if status is not None:
								self.signalInterface.send("contact_statusReceived",(fromJid, status))

							#self.sendNotificationReceived(notificationTo, notificationId, fromJid, participant, notificationType, None)

						elif notificationType == "subject":
							receiptRequested = True;

							bodyNode = node.getChild("body");
							newSubject = None if bodyNode is None else (bodyNode.data if sys.version_info < (3, 0) else bodyNode.data.encode('latin-1').decode());
							
							if newSubject is not None:
								self.signalInterface.send("group_subjectReceived",(msgId, fromAttribute, author, newSubject, int(attribute_t),  receiptRequested))

							#self.sendNotificationReceived(notificationTo, notificationId, fromJid, participant, notificationType, None)

						elif notificationType == "contacts":
							contactNode = node.getChild("add")
							contactJid = contactNode.getAttributeValue("jid")
							self.signalInterface.send("notification_contactAdded", (contactJid, ))
								
							contactsNode = ProtocolTreeNode("sync", {"contacts": "out"})
							#self.sendNotificationReceived(fromJid, notificationId, notificationTo, participant, notificationType, contactsNode)

					elif ProtocolTreeNode.tagEquals(node, "receipt"):
						receiptType = node.getAttributeValue("type");
						fromJid = node.getAttributeValue("from");
						msg_id = node.getAttributeValue("id")
						participant = node.getAttributeValue("participant")
						if receiptType == "delivered" or receiptType == "played" or receiptType != "":
							self.sendReceiptAck(msg_id, receiptType)
						if fromJid[-9:] == "broadcast":
							self.signalInterface.send("receipt_messageDelivered", (participant, msg_id))
						else:
							self.signalInterface.send("receipt_messageDelivered", (fromJid, msg_id))

					elif ProtocolTreeNode.tagEquals(node, "ack"):
						ackClass = node.getAttributeValue("class")
						if ackClass == "message":
							fromAttribute = node.getAttributeValue("from")
							msgId = node.getAttributeValue("id")
							self.signalInterface.send("receipt_messageSent", (fromAttribute, msgId))
						elif ackClass == "receipt":
							self._d("ack receipt not implemented")

					elif ProtocolTreeNode.tagEquals(node, "chatstate"):
						fromAttribute = node.getAttributeValue("from")
						composingNode = node.getChild("composing");
						if composingNode is not None:
							self.signalInterface.send("contact_typing", (fromAttribute, ))
						pausedNode = node.getChild("paused");
						if pausedNode is not None:
							self.signalInterface.send("contact_paused", (fromAttribute, ))


					elif ProtocolTreeNode.tagEquals(node,"message"):
						self.parseMessage(node)


		self._d("Reader thread terminating now!")

	def parseResultNode(self,node):
		typeval = node.getAttributeValue("type");
		if typeval != "result":
			idx = node.getAttributeValue("id")
			self._d("error response: " + idx)

	def parseOfflineMessageStamp(self,stamp):

		watime = WATime();
		parsed = watime.parseIso(stamp)
		local = watime.utcToLocal(parsed)
		stamp = watime.datetimeToTimestamp(local)

		return stamp


	def parsePingResponse(self, node):
		idx = node.getAttributeValue("id")


	def parseLastOnline(self,node):
		jid = node.getAttributeValue("from");
		firstChild = node.getChild(0);

		if "error" in firstChild.toString():
			return

		ProtocolTreeNode.require(firstChild,"query");
		seconds = firstChild.getAttributeValue("seconds");
		status = None
		status = firstChild.data #@@TODO discarded?

		try:
			if seconds is not None and jid is not None:
				self.signalInterface.send("presence_updated", (jid, int(seconds)))
		except:
			self._d("Ignored exception in handleLastOnline "+ sys.exc_info()[1])


	def parseGroups(self,node):
		children = node.getAllChildren("group");
		for groupNode in children:
			jid = groupNode.getAttributeValue("id") + "@g.us"
			owner = groupNode.getAttributeValue("owner")
			subject = groupNode.getAttributeValue("subject") if sys.version_info < (3, 0) else groupNode.getAttributeValue("subject").encode('latin-1').decode() 
			subjectT = groupNode.getAttributeValue("s_t")
			subjectOwner = groupNode.getAttributeValue("s_o")
			creation = groupNode.getAttributeValue("creation")

			self.signalInterface.send("group_gotInfo",(jid, owner, subject, subjectOwner, int(subjectT),int(creation)))


	def parseGroupInfo(self,node):
		jid = node.getAttributeValue("from");
		groupNode = node.getChild(0)
		if "error code" in groupNode.toString():
			self.signalInterface.send("group_infoError",(0,)) #@@TODO replace with real error code
		else:
			ProtocolTreeNode.require(groupNode,"group")
			#gid = groupNode.getAttributeValue("id")
			owner = groupNode.getAttributeValue("owner")
			subject = groupNode.getAttributeValue("subject") if sys.version_info < (3, 0) else groupNode.getAttributeValue("subject").encode('latin-1').decode();
			subjectT = groupNode.getAttributeValue("s_t")
			subjectOwner = groupNode.getAttributeValue("s_o")
			creation = groupNode.getAttributeValue("creation")
		
			self.signalInterface.send("group_gotInfo",(jid, owner, subject, subjectOwner, int(subjectT),int(creation)))

	def parseAddedParticipants(self, node):
		jid = node.getAttributeValue("from");
		jids = []
		
		addNodes = node.getAllChildren("add")

		for a in addNodes:
			t = a.getAttributeValue("type")
			if t == "success":
				jids.append(a.getAttributeValue("participant"))
			else:
				self._d("Failed to add %s" % jids.append(a.getAttributeValue("participant")))
		
		self.signalInterface.send("group_addParticipantsSuccess", (jid, jids))


	def parseRemovedParticipants(self,node): #fromm, successVector=None,failTable=None
		jid = node.getAttributeValue("from");
		jids = []
		
		addNodes = node.getAllChildren("remove")

		for a in addNodes:
			t = a.getAttributeValue("type")
			if t == "success":
				jids.append(a.getAttributeValue("participant"))
			else:
				self._d("Failed to add %s" % jids.append(a.getAttributeValue("participant")))
		self._d("handleRemovedParticipants DONE!");

		self.signalInterface.send("group_removeParticipantsSuccess", (jid, jids))

	def parseGroupCreated(self,node):
		jid = node.getAttributeValue("from");
		groupNode = node.getChild(0)
		
		if ProtocolTreeNode.tagEquals(groupNode,"error"):
			errorCode = groupNode.getAttributeValue("code")
			self.signalInterface.send("group_createFail", (errorCode,))
			return

		ProtocolTreeNode.require(groupNode,"group")
		group_id = groupNode.getAttributeValue("id")
		self.signalInterface.send("group_createSuccess", (group_id + "@g.us",))

	def parseGroupEnded(self,node):
		#jid = node.getAttributeValue("from");
		
		leaveNode = node.getChild(0)
		groupNode = leaveNode.getChild(0)
		
		jid = groupNode.getAttributeValue("id")
		
		self.signalInterface.send("group_endSuccess", (jid,))

	def parseGroupSubject(self,node):
		jid = node.getAttributeValue("from");
		self.signalInterface.send("group_setSubjectSuccess", (jid,))

	def parseParticipants(self,node):
		jid = node.getAttributeValue("from");
		children = node.getAllChildren("participant");
		jids = []
		for c in children:
			jids.append(c.getAttributeValue("jid"))

		self.signalInterface.send("group_gotParticipants", (jid, jids))

	#@@TODO PICTURE STUFF


	def createTmpFile(self, data, mode = "w"):
		
		tmp = tempfile.mkstemp()[1]
		
		tmpfile = open(tmp, mode)
		tmpfile.write(data)
		tmpfile.close()

		return tmp
	
	def parseSync(self, node):
		node_in = node.getChild("sync").getChild("in").getAllChildren("user")
		node_out = node.getChild("sync").getChild("out").getAllChildren("user")
		
		_in = [item.data for item in node_in]
		_out = [item.data for item in node_out]
		
		# Uncomment the following lines if you would rather return the jid
		# instead of the (international) phone number.
		# _in = [item.getAttributeValue("jid") for item in node_in]
		# _out = [item.getAttributeValue("jid") for item in node_out]
		
		self.signalInterface.send("sync_gotSyncResult", (_in, _out))
		
	
	def parseGetPicture(self,node):
		jid = node.getAttributeValue("from");
		if "error code" in node.toString():
			return;

		pictureNode = node.getChild("picture")
		if pictureNode.data is not None:
			tmp = self.createTmpFile(pictureNode.data if sys.version_info < (3, 0) else pictureNode.data.encode('latin-1'), "wb")

			pictureId = int(pictureNode.getAttributeValue('id'))
			try:
				jid.index('-')
				self.signalInterface.send("group_gotPicture", (jid, pictureId, tmp))
			except ValueError:
				self.signalInterface.send("contact_gotProfilePicture", (jid, pictureId, tmp))


	def parseGetPictureIds(self,node):
		jid = node.getAttributeValue("from");
		groupNode = node.getChild("list")
		#self._d(groupNode.toString())
		children = groupNode.getAllChildren("user");
		#pids = []
		for c in children:
			if c.getAttributeValue("id") is not None:
				#pids.append({"jid":c.getAttributeValue("jid"),"id":c.getAttributeValue("id")})
				self.signalInterface.send("contact_gotProfilePictureId", (c.getAttributeValue("jid"), c.getAttributeValue("id")))
		#self.signalInterface.send("contact_gotProfilePictureIds", (pids,))


	def parseSetPicture(self,node):
		jid = node.getAttributeValue("from");
		picNode = node.getChild("picture")
		
		try:
			jid.index('-')
			
			if picNode is None:
				self.signalInterface.send("group_setPictureError", (jid,0)) #@@TODO SEND correct error code
			else:
				pictureId = int(picNode.getAttributeValue("id"))
				self.signalInterface.send("group_setPictureSuccess", (jid, pictureId))
		except ValueError:
			if picNode is None:
				self.signalInterface.send("profile_setPictureError", (0,)) #@@TODO SEND correct error code
			else:
				pictureId = int(picNode.getAttributeValue("id"))
				self.signalInterface.send("profile_setPictureSuccess", (pictureId,))
	
	
	def parseRequestUpload(self, iqNode, _hash):

		mediaNode = iqNode.getChild("media")
		
		
		if mediaNode:

			url = mediaNode.getAttributeValue("url")
			
			resumeFrom = mediaNode.getAttributeValue("resume")
			
			if not resumeFrom:
				resumeFrom = 0
	
			if url:
				self.signalInterface.send("media_uploadRequestSuccess", (_hash, url, resumeFrom))
			else:
				self.signalInterface.send("media_uploadRequestFailed", (_hash,))
		else:
			duplicateNode = iqNode.getChild("duplicate")
			
			if duplicateNode:
				
				url = duplicateNode.getAttributeValue("url")
				
				
				self.signalInterface.send("media_uploadRequestDuplicate", (_hash, url))
		
			else:
				self.signalInterface.send("media_uploadRequestFailed", (_hash,))
				
	def parseSyncContacts(self, node):
		syncNode = node.getChild("sync")
		childs = []
		syncList = []
		if syncNode is not None:
			fullNode = syncNode.getChild("full")
			if fullNode is not None:
				childs += fullNode.getAllChildren()
			inNode = syncNode.getChild("in")
			if inNode is not None:
				childs += inNode.getAllChildren()
		for child in childs:
			if ProtocolTreeNode.tagEquals(child, "user"):
				cjid = child.getAttributeValue("jid")
				cphone = child.data
				syncList.append({"jid": cjid, "phone": cphone})
		if len(syncList) > 0:
			self.signalInterface.send("sync_contactsReceived", (syncList,))


	def parseSyncStatuses(self, node):
		syncNode = node.getChild("sync")
		childs = node.getAllChildren()
		syncList = []
		for child in childs:
			if ProtocolTreeNode.tagEquals(child, "user"):
				cjid = child.getAttributeValue("jid")
				timestamp = child.getAttributeValue("t")
				message = child.data
				if len(message) == 0:
					code = child.getAttributeValue("code")
					if code == "401":
						message = "hidden"
				syncList.append({"jid": cjid, "lastseen": timestamp, "message": message})
		if len(syncList) > 0:
			self.signalInterface.send("sync_statusesReceived", (syncList,))

	def parsePrivacyList(self, node):
		listNode = node.getChild("list")
		privacyList = []
		if listNode is not None:
			childs = listNode.getAllChildren()
			for child in childs:
				if ProtocolTreeNode.tagEquals(child, "item"):
					cjid = child.getAttributeValue("jid")
					if cjid is not None:
						privacyList.append(cjid)
		if len(privacyList) > 0:
			self.signalInterface.send("privacy_listReceived", (privacyList,))

	def parsePrivacySettings(self, node):
		settingsList = []
		childs = node.getAllChildren()
		for child in childs:
			if ProtocolTreeNode.tagEquals(node, "category"):
				key = child.getAttributeValue("name")
				value = child.getAttributeValue("value")
				settingsList.append({"key": key, "value": value})
		if len(settingsList) > 0:
			self.signalInterface.send("privacy_settingsReceived", (settingsList,))

	def parseAccountDelete(self, node):
		#TODO
		self._d("parseAccountDelete not implemented")

	def parseMessage(self,messageNode):
		id = messageNode.getAttributeValue("id");
		timestamp = int(messageNode.getAttributeValue("t"))
		fromAttribute = messageNode.getAttributeValue("from");
		author = messageNode.getAttributeValue("participant");
		isBroadcast = False;
		if fromAttribute.find("@broadcast") >= 0:
			fromAttribute = author;
			isBroadcast = True;
		
		offline = messageNode.getAttributeValue("offline") is not None
		retry = messageNode.getAttributeValue("retry");
		typeAttribute = messageNode.getAttributeValue("type");

		msgData = None
		isGroup = False
		
		bodyNode = messageNode.getChild("body");
		newSubject = "" if bodyNode is None else bodyNode.data;
		if newSubject.find("New version of WhatsApp Messenger is now available")>-1:
			self._d("Rejecting whatsapp server message")
			return #REJECT THIS FUCKING MESSAGE!

		try:
			fromAttribute.index('-')
			isGroup = True
		except:
			pass

		pushName = None
		notifNode = messageNode.getChild("notify")
		if notifNode is not None:
			pushName = notifNode.getAttributeValue("name");


		msgId = messageNode.getAttributeValue("id");

		if typeAttribute == "error":
			errorCode = 0;
			errorNodes = messageNode.getAllChildren("error");
			for errorNode in errorNodes:
				codeString = errorNode.getAttributeValue("code")
				try:
					errorCode = int(codeString);
				except ValueError:
					'''catch value error'''
				self.signalInterface.send("message_error", (msgId, fromAttribute, errorCode))

		elif typeAttribute == "text" or typeAttribute == "media":
			wantsReceipt = False;
			messageChildren = [] if messageNode.children is None else messageNode.children

			for childNode in messageChildren:
				if ProtocolTreeNode.tagEquals(childNode,"request"):
					wantsReceipt = True;

				elif ProtocolTreeNode.tagEquals(childNode,"media") and msgId is not None:
	
					self._d("MULTIMEDIA MESSAGE!");
					
					mediaUrl = messageNode.getChild("media").getAttributeValue("url");
					mediaType = messageNode.getChild("media").getAttributeValue("type")
					mediaSize = messageNode.getChild("media").getAttributeValue("size")
					encoding = messageNode.getChild("media").getAttributeValue("encoding")
					mediaPreview = None


					if mediaType == "image":
						mediaPreview = messageNode.getChild("media").data
						
						if encoding == "raw" and mediaPreview:
							mediaPreview = base64.b64encode(mediaPreview) if sys.version_info < (3, 0) else base64.b64encode(mediaPreview.encode('latin-1')).decode()

						if isGroup:
							self.signalInterface.send("group_imageReceived", (msgId, fromAttribute, author, mediaPreview, mediaUrl, mediaSize, wantsReceipt))
						else:
							self.signalInterface.send("image_received", (msgId, fromAttribute, mediaPreview, mediaUrl, mediaSize,  wantsReceipt, isBroadcast))

					elif mediaType == "video":
						mediaPreview = messageNode.getChild("media").data
						
						if encoding == "raw" and mediaPreview:
							mediaPreview = base64.b64encode(mediaPreview) if sys.version_info < (3, 0) else base64.b64encode(mediaPreview.encode('latin-1')).decode()

						if isGroup:
							self.signalInterface.send("group_videoReceived", (msgId, fromAttribute, author, mediaPreview, mediaUrl, mediaSize, wantsReceipt))
						else:
							self.signalInterface.send("video_received", (msgId, fromAttribute, mediaPreview, mediaUrl, mediaSize, wantsReceipt, isBroadcast))

					elif mediaType == "audio":
						mediaPreview = messageNode.getChild("media").data

						if isGroup:
							self.signalInterface.send("group_audioReceived", (msgId, fromAttribute, author, mediaUrl, mediaSize, wantsReceipt))
						else:
							self.signalInterface.send("audio_received", (msgId, fromAttribute, mediaUrl, mediaSize, wantsReceipt, isBroadcast))

					elif mediaType == "location":
						mlatitude = messageNode.getChild("media").getAttributeValue("latitude")
						mlongitude = messageNode.getChild("media").getAttributeValue("longitude")
						name = messageNode.getChild("media").getAttributeValue("name")
						
						if name and not sys.version_info < (3, 0):
							name = name.encode('latin-1').decode()
						
						mediaPreview = messageNode.getChild("media").data
						
						if encoding == "raw" and mediaPreview:
							mediaPreview = base64.b64encode(mediaPreview) if sys.version_info < (3, 0) else base64.b64encode(mediaPreview.encode('latin-1')).decode()

						if isGroup:
							self.signalInterface.send("group_locationReceived", (msgId, fromAttribute, author, name or "", mediaPreview, mlatitude, mlongitude, wantsReceipt))
						else:
							self.signalInterface.send("location_received", (msgId, fromAttribute, name or "", mediaPreview, mlatitude, mlongitude, wantsReceipt, isBroadcast))
		
					elif mediaType =="vcard":
						#return
						#mediaItem.preview = messageNode.getChild("media").data
						vcardData = messageNode.getChild("media").getChild("vcard").data
						vcardName = messageNode.getChild("media").getChild("vcard").getAttributeValue("name")
						
						if vcardName and not sys.version_info < (3, 0):
							vcardName = vcardName.encode('latin-1').decode()
						
						if vcardData is not None:
							n = vcardData.find(">") +1
							vcardData = vcardData[n:]
							vcardData = vcardData.replace("</vcard>","")

							if isGroup:
								self.signalInterface.send("group_vcardReceived", (msgId, fromAttribute, author, vcardName, vcardData, wantsReceipt))
							else:
								self.signalInterface.send("vcard_received", (msgId, fromAttribute, vcardName, vcardData, wantsReceipt, isBroadcast))
							
					else:
						self._d("Unknown media type")
						return

				elif ProtocolTreeNode.tagEquals(childNode,"body") and msgId is not None:
					msgData = childNode.data;
					
					#fmsg.setData({"status":0,"key":key.toString(),"content":msgdata,"type":WAXMPP.message_store.store.Message.TYPE_RECEIVED});

				elif ProtocolTreeNode.tagEquals(childNode,"received") and fromAttribute is not None and msgId is not None:

					if fromAttribute == "s.us":
						self.signalInterface.send("profile_setStatusSuccess", ("s.us", msgId,))
						return;

					#@@TODO autosend ack from client
					#print "NEW MESSAGE RECEIVED NOTIFICATION!!!"
					#self.connection.sendDeliveredReceiptAck(fromAttribute,msg_id);
					self.signalInterface.send("receipt_messageDelivered", (fromAttribute, msgId))
					
					return


				elif not (ProtocolTreeNode.tagEquals(childNode,"active")):
					if ProtocolTreeNode.tagEquals(childNode,"request"):
						wantsReceipt = True;

					elif ProtocolTreeNode.tagEquals(childNode,"notify"):
						notify_name = childNode.getAttributeValue("name");


					elif ProtocolTreeNode.tagEquals(childNode,"delay"):
						xmlns = childNode.getAttributeValue("xmlns");
						if "urn:xmpp:delay" == xmlns:
							stamp_str = childNode.getAttributeValue("stamp");
							if stamp_str is not None:
								stamp = stamp_str
								timestamp = self.parseOfflineMessageStamp(stamp)*1000;

					elif ProtocolTreeNode.tagEquals(childNode,"x"):
						xmlns = childNode.getAttributeValue("xmlns");
						if "jabber:x:event" == xmlns and msgId is not None:
							
							if fromAttribute == "broadcast":
								self.signalInterface.send("receipt_broadcastSent", (msgId,))
							else:
								self.signalInterface.send("receipt_messageSent", (fromAttribute, msgId))

						elif "jabber:x:delay" == xmlns:
							continue; #@@TODO FORCED CONTINUE, WHAT SHOULD I DO HERE? #wtf?
							stamp_str = childNode.getAttributeValue("stamp");
							if stamp_str is not None:
								stamp = stamp_str
								timestamp = stamp;
					else:
						if ProtocolTreeNode.tagEquals(childNode,"delay") or not ProtocolTreeNode.tagEquals(childNode,"received") or msgId is None:
							continue;

							
							receipt_type = childNode.getAttributeValue("type");
							if receipt_type is None or receipt_type == "delivered":
								self.signalInterface.send("receipt_messageDelivered", (fromAttribute, msgId))
							elif receipt_type == "visible":
								self.signalInterface.send("receipt_visible", (fromAttribute, msgId))

			if msgData:
				msgData = msgData if sys.version_info < (3, 0) else msgData.encode('latin-1').decode()
				if isGroup:
					self.signalInterface.send("group_messageReceived", (msgId, fromAttribute, author, msgData, timestamp, wantsReceipt, pushName))

				else:
					self.signalInterface.send("message_received", (msgId, fromAttribute, msgData, timestamp, wantsReceipt, pushName, isBroadcast))

				##@@TODO FROM CLIENT
				'''if conversation.type == "group":
					if conversation.subject is None:
						signal = False
						self._d("GETTING GROUP INFO")
						self.connection.sendGetGroupInfo(fromAttribute)
				'''
					#if not len(conversation.getContacts()):
					#	self._d("GETTING GROUP CONTACTS")
					#	self.connection.sendGetParticipants(fromAttribute)

				'''@@TODO FROM CLIENT
				if ret is None:
					conversation.incrementNew();
					WAXMPP.message_store.pushMessage(fromAttribute,fmsg)
					fmsg.key = key
				else:
					fmsg.key = eval(ret.key)
					duplicate = True;
				'''
			
