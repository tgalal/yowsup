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


import threading
class SignalInterfaceBase(object):

	signals = [	
			
			"auth_success",
			"auth_fail",
			
			"message_received", #k
			"image_received",
			"vcard_received",
			"video_received",
			"audio_received",
			"location_received",
			
			"message_error",

			"receipt_messageSent", #k
			"receipt_messageDelivered", #k
			"receipt_visible", #k
			"receipt_broadcastSent",
			"status_dirty",

			"presence_updated", #k
			"presence_available", #k
			"presence_unavailable", #k
			
			"group_subjectReceived",
			"group_createSuccess",
			"group_createFail",
			"group_endSuccess",
			"group_gotInfo",
			"group_infoError",
			"group_addParticipantsSuccess",
			"group_removeParticipantsSuccess",
			"group_gotParticipants",
			"group_setSubjectSuccess",
			"group_messageReceived",
			"group_imageReceived",
			"group_vcardReceived",
			"group_videoReceived",
			"group_audioReceived",
			"group_locationReceived",
			"group_setPictureSuccess",
			"group_setPictureError",
			"group_gotPicture",
			"group_gotGroups",			
			
			"notification_contactProfilePictureUpdated",
			"notification_contactProfilePictureRemoved",
			"notification_groupPictureUpdated",
			"notification_groupPictureRemoved",
			"notification_groupParticipantAdded",
			"notification_groupParticipantRemoved",
			"notification_contactAdded",

			"contact_gotProfilePictureId",
			"contact_gotProfilePicture",
			"contact_typing",
			"contact_paused",
			"contact_statusReceived",
			
			"profile_setPictureSuccess",
			"profile_setPictureError",
			"profile_setStatusSuccess",
			
			"sync_gotSyncResult",

			"ping",
			"pong",
			"disconnected",

			"subscription_link",

			"privacy_listReceived",

			"privacy_settingsReceived",

			"sync_contactsReceived",
			"sync_statusesReceived",
			
			"media_uploadRequestSuccess",
			"media_uploadRequestFailed",
			"media_uploadRequestDuplicate"
		]
	
	def __init__(self):#@@TODO unified naming pattern
		self.registeredSignals = {}
	
	def getSignals(self):
		return self.signals

	def registerListener(self,signalName, callback):
		if self.hasSignal(signalName):
			if self.isRegistered(signalName):
				self.registeredSignals[signalName].append(callback)
			else:
				self.registeredSignals[signalName] = [callback]
				
	def _sendAsync(self, signalName, args=()):
		#print "Sending signal %s" % signalName
		listeners = self.getListeners(signalName)
		for l in listeners:
			threading.Thread(target = l, args = args).start()

	def send(self, signalName, args = ()):
		self._sendAsync(signalName, args)
	
	def getListeners(self, signalName):
		if self.hasSignal(signalName):
			
			
			try:
				self.registeredSignals[signalName]
				return self.registeredSignals[signalName]
			except KeyError:
				pass

		return []

	def isRegistered(self, signalName):
		try:
			self.registeredSignals[signalName]
			return True
		except KeyError:
			return False
	
	def hasSignal(self, signalName):
		try:
			self.signals.index(signalName)
			return True

		except ValueError:
			return False

class MethodInterfaceBase(object):

	methods = [	
			"getVersion",

			"auth_login",
			"message_send", #B
			"message_imageSend",
			"message_audioSend",
			"message_videoSend",
			"message_locationSend",
			"message_vcardSend",

			"message_ack", #BF

			"notification_ack",

			"clientconfig_send",

			"delivered_ack", #B

			"visible_ack", #B

			"ping", #B
			"pong", #B

			"typing_send", #B
			"typing_paused", #B

			"subject_ack", #B

			"group_getGroups",
			"group_getInfo",
			"group_create",
			"group_addParticipants",
			"group_removeParticipants",
			"group_end",
			"group_setSubject",
			"group_setPicture",
			"group_getParticipants",
			"group_getPicture",

			"picture_get",
			"picture_getIds",

			"contact_getProfilePicture",

			"presence_request", #B
			"presence_unsubscribe", #B
			"presence_subscribe", #B
			"presence_sendAvailableForChat", #B
			"presence_sendAvailable", #B
			"presence_sendUnavailable", #B
			
			"profile_getPicture",
			"profile_setPicture",
			"profile_setStatus",

			"sync_sendSync",
			
			"ready",
			"disconnect",
			
			"message_broadcast",
			
			"media_requestUpload"
			]
	def __init__(self):
		self.registeredMethods = {}


	def call(self, methodName, params=()):
		#print "SHOULD CALL"
		#print methodName
		callback = self.getCallback(methodName)
		if callback:
			return callback(*params)
		#@@TODO raise no method exception
		return None

	def getMethods(self):
		return self.methods

	def getCallback(self, methodName):
		if self.hasMethod(methodName):
			return self.registeredMethods[methodName]

		return None

	def isRegistered(self, methodName):
		try:
			self.registeredMethods[methodName]
			return True
		except KeyError:
			return False
	
	def registerCallback(self, methodName, callback):
		if self.hasMethod(methodName):
			self.registeredMethods[methodName] = callback

	def hasMethod(self, methodName):
		try:
			self.methods.index(methodName)
			return True

		except ValueError:
			return False
