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

import urllib,sys, os

if sys.version_info < (3, 0):
	import httplib
	from urllib import urlencode
else:
	from http import client as httplib
	from urllib.parse import urlencode

import hashlib
from .waresponseparser import ResponseParser
from Yowsup.Common.debugger import Debugger as WADebug
from Yowsup.Common.constants import Constants
from Yowsup.Common.utilities import Utilities

class WARequest(object):

	OK = 200

	#moved to Constants

	def __init__(self):
		WADebug.attach(self)

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

	def removeParam(self, name):
		for i in range(0, len(self.params)):
			if self.params[i][0] == name:
				del self.params[i]


	def addHeaderField(self, name, value):
		self.headers[name] = value;

	def clearParams(self):
		self.params = []

	def getUserAgent(self):

		tokenData = Utilities.readToken()

		if tokenData:
			agent = tokenData["u"]
		else:
			agent = Constants.tokenData["u"]
		return agent

	def getToken(self, phone, token):
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

		if len(headers):
			WADebug.stdDebug(headers)
		if len(params):
			WADebug.stdDebug(params)

		WADebug.stdDebug("Opening connection to %s" % host);

		conn = httplib.HTTPSConnection(host ,port) if port == 443 else httplib.HTTPConnection(host ,port)

		WADebug.stdDebug("Sending %s request to %s" % (reqType, path))
		conn.request(reqType, path, params, headers);

		response = conn.getresponse()

		return response
