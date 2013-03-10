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

import urllib,sys

if sys.version_info < (3, 0):
	import httplib
	from urllib import urlencode
else:
	from http import client as httplib
	from urllib.parse import urlencode

import hashlib
from .waresponseparser import ResponseParser
from Yowsup.Common.debugger import Debugger as WADebug

class WARequest(object):
	
	UserAgents = [
			("WhatsApp/2.8.2 WP7/7.10.8773.98 Device/NOKIA-Lumia_800-H112.1402.2.3", 
				"k7Iy3bWARdNeSL8gYgY6WveX12A1g4uTNXrRzt1H"+"889d4f44e479e6c38b4a834c6d8417815f999abe{phone}"),
			
			("WhatsApp/2.3.53 S40Version/14.26 Device/Nokia302", 
				"PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk" + "1354754753509{phone}"),
				
			("WhatsApp/2.4.7 S40Version/14.26 Device/Nokia302", 
				"PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk" + "1359594496554{phone}")
		]
	
	OK = 200

	def __init__(self):
		WADebug.attach(self)
		
		self.uaIndex = 2;
		self.pvars = [];
		self.port = 443;
		self.type = "GET"
		self.parser = None
		self.params = []
		self.headers = {}
		
		self.sent = False
		self.response = None
	

	
	def setParsableVariables(self, pvars):
		self.pvars = pvars;
	
	def onResponse(self, name, value):
		if name == "status":
			self.status = value
		elif name == "result":
			self.result = value
			
	def addParam(self,name,value):
		self.params.append((name,value.encode('utf-8')))
		
	def addHeaderField(self, name, value):
		self.headers[name] = value;

	def clearParams(self):
		self.params = []

	def getUserAgent(self):
		return WARequest.UserAgents[self.uaIndex][0]
	
	def getToken(self, phone):

		token = WARequest.UserAgents[self.uaIndex][1]
		
		return hashlib.md5(token.format(phone=phone).encode()).hexdigest()
	
	def send(self, parser = None):
		
		if self.type == "POST":
			return self.sendPostRequest(parser)
		
		return self.sendGetRequest(parser)
		
	def setParser(self, parser):
		if isinstance(parser, ResponseParser):
			self.parser = parser
		else:
			self._d("Invalid parser")
	
	def getConnectionParameters(self):
		
		if not self.url:
			return ("", "", self.port)

		try:
			url = self.url.split("://", 1)
			url = url[0] if len(url) == 1 else url[1]
			
			host, path = url.split('/', 1)
		except ValueError:
			host = url
			path = ""
		
		path = "/" + path
		
		return (host, self.port, path)
	
	def sendGetRequest(self, parser = None):
		self.response = None
		params =  self.params#[param.items()[0] for param in self.params];
		
		parser = parser or self.parser or ResponseParser()
		
		headers = dict(list({"User-Agent":self.getUserAgent(),
				"Accept": parser.getMeta()
			}.items()) + list(self.headers.items()));

		host,port,path = self.getConnectionParameters()
		self.response = WARequest.sendRequest(host, port, path, headers, params, "GET")
		
		if not self.response.status == WARequest.OK:
			self._d("Request not success, status was %s"%self.response.status)
			return {}

		data = self.response.read()
		self._d(data);
		
		self.sent = True
		return parser.parse(data.decode(), self.pvars)
	
	def sendPostRequest(self, parser = None):
		self.response = None
		params =  self.params #[param.items()[0] for param in self.params];
		
		parser = parser or self.parser or ResponseParser()
		
		headers = dict(list({"User-Agent":self.getUserAgent(),
				"Accept": parser.getMeta(),
				"Content-Type":"application/x-www-form-urlencoded"
			}.items()) + list(self.headers.items()));
	
		host,port,path = self.getConnectionParameters()
		self.response = WARequest.sendRequest(host, port, path, headers, params, "POST")
		
		
		if not self.response.status == WARequest.OK:
			self._d("Request not success, status was %s"%self.response.status)
			return {}

		data = self.response.read()
		
		self._d(data);
		
		self.sent = True
		return parser.parse(data.decode(), self.pvars)
	
	
	@staticmethod
	def sendRequest(host, port, path, headers, params, reqType="GET"):

		params = urlencode(params);

		
		path = path + "?"+ params if reqType == "GET" else path
		
		WADebug.stdDebug(reqType)
		WADebug.stdDebug(headers);
		WADebug.stdDebug(params);

		WADebug.stdDebug("Opening connection to %s" % host);
		
		conn = httplib.HTTPSConnection(host ,port) if port == 443 else httplib.HTTPConnection(host ,port)
		
		WADebug.stdDebug("Requesting %s" % path)
		conn.request(reqType, path, params, headers);

		response = conn.getresponse()
		
		#WADebug.stdDebug(response)

		return response
