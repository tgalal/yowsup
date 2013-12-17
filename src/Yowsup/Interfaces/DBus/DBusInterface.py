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

import dbus.service

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__+"/..")))
os.sys.path.insert(0,parentdir)

from Interfaces.Interface import SignalInterfaceBase, MethodInterfaceBase
from connectionmanager import YowsupConnectionManager


class DBusInitInterface(dbus.service.Object):
	DBUS_INTERFACE = "com.yowsup.methods"
	def __init__(self):
		self.busName = dbus.service.BusName(self.DBUS_INTERFACE, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self,self.busName, '/com/yowsup/methods')
		
		self.connections = {}
		
		super(DBusInitInterface, self).__init__()
		
	@dbus.service.method(DBUS_INTERFACE)
	def init(self, username):
		man = YowsupConnectionManager()
		man.setInterfaces(DBusSignalInterface(username), DBusMethodInterface(username))
		self.connections[username] = man
		
		return username
		

class DBusSignalInterface(SignalInterfaceBase, dbus.service.Object):

	DBUS_INTERFACE = "com.yowsup.signals"
	
	def __init__(self, connectionId):
		self.connectionId = connectionId
		self.busName = dbus.service.BusName(self.DBUS_INTERFACE, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, self.busName, '/com/yowsup/%s/signals'%connectionId)

		super(DBusSignalInterface,self).__init__();

		self._attachDbusSignalsToSignals()


	@dbus.service.method(DBUS_INTERFACE)
	def getSignals(self):
		return self.signals
	
	def _attachDbusSignalsToSignals(self):
		for s in self.signals:
			try:
				currBusSig = getattr(self, s)
				self.registerListener(s, currBusSig)
				print("Registered %s on Dbus " % s)
			except AttributeError:
				print("Skipping %s" %s)

	## Signals ##
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def auth_success(self, username):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def auth_fail(self, username, reason):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def presence_updated(self, jid, lastSeen):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def presence_available(self, jid):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def presence_unavailable(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def message_received(self, msgId, jid, content, timestamp, wantsReceipt, isBroadcast):
		pass
#--------------------------------------------------------------------------- Groups
	@dbus.service.signal(DBUS_INTERFACE)
	def group_messageReceived(self, msgId, jid, author, content, timestamp, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotInfo(self, jid, owner, subject, subjectOwner, subjectT, creation):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setSubjectSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_subjectReceived(self, msgId, fromAttribute, author, newSubject, timestamp, receiptRequested):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_addParticipantsSuccess(self, jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_removeParticipantsSuccess(self, jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_createSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_createFail(self, errorCode):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_endSuccess(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotPicture(self, jid, pictureId, filepath):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_infoError(self, errorCode):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_gotParticipants(self,jid, jids):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setPictureSuccess(self, jid, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def group_setPictureError(self, jid, errorCode):
		pass
	
#------------------------------------------------------------------------------ 
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setStatusSuccess(self, jid, messageId):
		pass
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setPictureSuccess(self, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def profile_setPictureError(self, errorCode):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def status_dirty(self):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_messageSent(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_messageDelivered(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def receipt_visible(self, jid, msgId):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def contact_gotProfilePictureId(self, jid, pictureId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_typing(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_paused(self, jid):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def contact_gotProfilePicture(self, jid, pictureId, filename):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def notification_contactProfilePictureUpdated(self, jid, timestamp, messageId, pictureId, wantsReceipt = True):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def notification_contactProfilePictureRemoved(self, jid, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupParticipantAdded(self, gJid, jid, author, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupParticipantRemoved(self, gjid, jid, author, timestamp, messageId, wantsReceipt = True):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupPictureUpdated(self, jid, author, timestamp, messageId, pictureId, wantsReceipt = True):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def notification_groupPictureRemoved(self, jid, author, timestamp, messageId, wantsReceipt = True):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def image_received(self, messageId, jid, preview, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def video_received(self, messageId, jid, preview, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def audio_received(self, messageId, jid, url, size, wantsReceipt, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def location_received(self, messageId, jid, name, preview, latitude, longitude, isBroadcast):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def vcard_received(self, messageId, jid, name, data, isBroadcast):
		pass


	@dbus.service.signal(DBUS_INTERFACE)
	def group_imageReceived(self, messageId, jid, author, preview, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_videoReceived(self, messageId, jid, author, preview, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_audioReceived(self, messageId, jid, author, url, size, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_locationReceived(self, messageId, jid, author, name, preview, latitude, longitude, wantsReceipt):
		pass

	@dbus.service.signal(DBUS_INTERFACE)
	def group_vcardReceived(self, messageId, jid, author, name, data, wantsReceipt):
		pass
	
	
	@dbus.service.signal(DBUS_INTERFACE)
	def message_error(self, messageId, jid, errorCode):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def disconnected(self, reason):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def ping(self, pingId):
		pass
	
	@dbus.service.signal(DBUS_INTERFACE)
	def pong(self):
		pass

	
		
class DBusMethodInterface(MethodInterfaceBase, dbus.service.Object):
	DBUS_INTERFACE = 'com.yowsup.methods'

	def __init__(self, connectionId):
		self.connectionId = connectionId
		super(DBusMethodInterface,self).__init__();

		busName = dbus.service.BusName(self.DBUS_INTERFACE, bus=dbus.SessionBus())
		dbus.service.Object.__init__(self, busName, '/com/yowsup/%s/methods'%connectionId)


	def interfaceMethod(fn):
		def wrapped(self, *args):
			fnName = fn.__name__
			return self.call(fnName, args)
		return wrapped

	@dbus.service.method(DBUS_INTERFACE)
	def getMethods(self):
		return self.methods
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def getVersion(self):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def auth_login(self, number, password):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_send(self, jid, message):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_imageSend(self, jid, url, name, size, preview):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_videoSend(self, jid, url, name, size, preview):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_audioSend(self, jid, url, name, size):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_locationSend(self, jid, latitude, longitude, preview): #@@TODO add name to location?
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_vcardSend(self, jid, data, name):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def message_ack(self, jid, msgId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def notification_ack(self, jid, msgId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def clientconfig_send(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def delivered_ack(self, jid, msgId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def visible_ack(self, jid, msgId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def ping(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def pong(self, pingId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def typing_send(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def typing_paused(self,jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def subject_ack(self, jid, msgId):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_getInfo(self,jid):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_getPicture(self,jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_create(self, subject):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_addParticipants(self, jid, participants):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_removeParticipants(self, jid, participants):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_setPicture(self, jid, filepath):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_end(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_setSubject(self, jid, subject):
		pass

	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def group_getParticipants(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_sendAvailable(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_request(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_sendUnavailable(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_sendAvailableForChat(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_subscribe(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def presence_unsubscribe(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def contact_getProfilePicture(self, jid):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def picture_getIds(self,jids):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def profile_getPicture(self):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def profile_setStatus(self, status):
		pass
	
	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def profile_setPicture(self, filepath):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def ready(self):
		pass

	@dbus.service.method(DBUS_INTERFACE)
	@interfaceMethod
	def disconnect(self, reason):
		pass

