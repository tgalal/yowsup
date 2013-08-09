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

			("WhatsApp/2.10.523 WP7/7.10.8858 Device/HTC-HTC-H0002", "Od52pFozHNWF9XbTN5lrqDtnsiZGL2G3l9yw1GiQ21a31a2d9dbdc9a8ce324ef2df918064fd26e30a{phone}"),
			("WhatsApp/2.10.750 Android/4.2.1 Device/GalaxyS3", 
			 "30820332308202f0a00302010202044c2536a4300b06072a8648ce3804030500307c310b3009060355040613025553311330110603550408130a43616c69666f726e6961311430120603550407130b53616e746120436c61726131163014060355040a130d576861747341707020496e632e31143012060355040b130b456e67696e656572696e67311430120603550403130b427269616e204163746f6e301e170d3130303632353233303731365a170d3434303231353233303731365a307c310b3009060355040613025553311330110603550408130a43616c69666f726e6961311430120603550407130b53616e746120436c61726131163014060355040a130d576861747341707020496e632e31143012060355040b130b456e67696e656572696e67311430120603550403130b427269616e204163746f6e308201b83082012c06072a8648ce3804013082011f02818100fd7f53811d75122952df4a9c2eece4e7f611b7523cef4400c31e3f80b6512669455d402251fb593d8d58fabfc5f5ba30f6cb9b556cd7813b801d346ff26660b76b9950a5a49f9fe8047b1022c24fbba9d7feb7c61bf83b57e7c6a8a6150f04fb83f6d3c51ec3023554135a169132f675f3ae2b61d72aeff22203199dd14801c70215009760508f15230bccb292b982a2eb840bf0581cf502818100f7e1a085d69b3ddecbbcab5c36b857b97994afbbfa3aea82f9574c0b3d0782675159578ebad4594fe67107108180b449167123e84c281613b7cf09328cc8a6e13c167a8b547c8d28e0a3ae1e2bb3a675916ea37f0bfa213562f1fb627a01243bcca4f1bea8519089a883dfe15ae59f06928b665e807b552564014c3bfecf492a0381850002818100d1198b4b81687bcf246d41a8a725f0a989a51bce326e84c828e1f556648bd71da487054d6de70fff4b49432b6862aa48fc2a93161b2c15a2ff5e671672dfb576e9d12aaff7369b9a99d04fb29d2bbbb2a503ee41b1ff37887064f41fe2805609063500a8e547349282d15981cdb58a08bede51dd7e9867295b3dfb45ffc6b259300b06072a8648ce3804030500032f00302c021400a602a7477acf841077237be090df436582ca2f0214350ce0268d07e71e55774ab4eacd4d071cd1efad"+
			 "022e923a364bfacff3a80de3f950b1e0"+
			 "{phone}"),

			("WhatsApp/2.8.2 WP7/7.10.8773.98 Device/NOKIA-Lumia_800-H112.1402.2.3", 
				"k7Iy3bWARdNeSL8gYgY6WveX12A1g4uTNXrRzt1H"+"889d4f44e479e6c38b4a834c6d8417815f999abe{phone}"),
			
			("WhatsApp/2.3.53 S40Version/14.26 Device/Nokia302", 
				"PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk" + "1354754753509{phone}"),
				
			("WhatsApp/2.4.7 S40Version/14.26 Device/Nokia302", 
				"PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk" + "1359594496554{phone}"),
		    
		    ("WhatsApp/2.4.22 S40Version/14.26 Device/Nokia302", 
				"PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk" + "1366850357035{phone}"),

		]
	
	OK = 200

	def __init__(self):
		WADebug.attach(self)
		
		self.uaIndex = 1;
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

		
		path = path + "?"+ params if reqType == "GET" and params else path
		
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
