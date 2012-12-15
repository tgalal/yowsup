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

import time

class Debugger():
	enabled = True
	def __init__(self):
		
		cname = self.__class__.__name__
		self.type= cname[:cname.index("Debug")]
	
	@staticmethod
	def attach(instance):
		d = Debugger()
		d.type = instance.__class__.__name__;
		instance._d = d.d
	
	@staticmethod
	def stdDebug(message,messageType="General"):
		#enabledTypes = ["general","stanzareader","sql","conn","waxmpp","wamanager","walogin","waupdater","messagestore"];
		
		if not Debugger.enabled:
			return
		
		disabledTypes = ["sql"]
		if messageType.lower() not in disabledTypes:
			try:
				print(message)
			except UnicodeEncodeError:
				print ("Skipped debug message because of UnicodeDecodeError")
	
	def formatMessage(self,message):
		#default = "{type}:{time}:\t{message}"
		t = time.time()
		message = "%s:\t%s"%(self.type,message)
		return message
	
	def debug(self,message):
		if Debugger.enabled:
			Debugger.stdDebug(self.formatMessage(message),self.type)
		
	def d(self,message):
		self.debug(message)