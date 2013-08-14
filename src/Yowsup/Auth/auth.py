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

from .mechanisms.wauth import WAuth as AuthMechanism

from Yowsup.Common.constants import Constants
from Yowsup.Common.debugger import Debugger

class YowsupAuth:
	def __init__(self, connection):
		Debugger.attach(self)

		self.connection = connection
		self.mechanism = AuthMechanism
		self.authenticated = False

		self.username = None
		self.password = None
		self.domain = None
		self.resource = None

		self.supportsReceiptAcks = True
		self.accountKind = None
		self.expireData = None

		self.authCallbacks = []

	def isAuthenticated(self):
		return self.authenticated

	def onAuthenticated(self, callback):
		self.authCallbacks.append(callback)

	def authenticationComplete(self):
		self.authenticated = True
		#should process callbacks

	def authenticationFailed(self):
		self._d("Authentication failed!!")

	def authenticate(self, username, password, domain, resource):
		self._d("Connecting to %s" % Constants.host)
		#connection = ConnectionEngine()
		self.connection.connect((Constants.host, Constants.port));

		
		self.mechanism = AuthMechanism(self.connection)
		self.mechanism.setAuthObject(self)

		self.username = username
		self.password = password
		self.domain = domain
		self.resource = resource
		self.jid = "%s@%s"%(self.username,self.domain)
		
	
		
		connection = self.mechanism.login(username, password, domain, resource)
		return connection
