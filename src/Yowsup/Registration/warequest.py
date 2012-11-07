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

import httplib,urllib
from Yowsup.Tools.debugger import Debugger as WADebug

class WARequest(object):


	#BASE_URL = [ 97, 61, 100, 123, 114, 103, 96, 114, 99, 99, 61, 125, 118, 103 ];
	status = None
	result = None
	params = []
	#v = "v1"
	#method = None
	conn = None
	
	def __init__(self):
		WADebug.attach(self)
	
	def onResponse(self, name, value):
		if name == "status":
			self.status = value
		elif name == "result":
			self.result = value
			
	def addParam(self,name,value):
		self.params.append({name:value.encode('utf-8')});

	def clearParams(self):
		self.params = []
	
	def getUrl(self):
		return  self.base_url+self.req_file;

	def getUserAgent(self):
		#agent = "WhatsApp/1.2 S40Version/microedition.platform";
		agent = "WhatsApp/2.8.2 WP7/7.10.8773.98 Device/NOKIA-Lumia_800-H112.1402.2.3";
		return agent;	

	def sendRequest(self):


		
		self.params =  [param.items()[0] for param in self.params];
		
		params = urllib.urlencode(self.params);
		
		self._d("Opening connection to "+self.base_url);
		self.conn = httplib.HTTPSConnection(self.base_url,443);
		headers = {"User-Agent":self.getUserAgent(),
			"Content-Type":"application/x-www-form-urlencoded",
			"Accept":"text/xml"
			};
		
		self._d(headers);
		self._d(params);
		
		self.conn.request("POST",self.req_file,params,headers);
		resp=self.conn.getresponse()
 		response=resp.read();
 		self._d(response);
 		#doc = minidom.parseString(response);
 		return response;
		#response_node  = doc.getElementsByTagName("response")[0];

		#for (name, value) in response_node.attributes.items():
		#self.onResponse(name,value);
