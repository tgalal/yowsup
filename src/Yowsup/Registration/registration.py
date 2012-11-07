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

from utilities import Utilities
from warequest import WARequest
import httplib,urllib
from xml.dom import minidom


			
class WACodeRequest(WARequest):
	def __init__(self,cc, p_in, method="sms"):
		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("to",cc+p_in);
		self.addParam("lc","GB");
		self.addParam("lg","en");
		self.addParam("mcc","602");
		self.addParam("mnc","002");
		self.addParam("imsi","602022009074736");
		self.addParam("method",method);
		self.base_url = "r.whatsapp.net"
		self.req_file = "/v1/code.php"
		
	def handleResponse(self,data):
		response_node  = data.getElementsByTagName("response")[0];

		for (name, value) in response_node.attributes.items():
			if name == "status":
				self.status = value
			elif name == "result":
				self.result = value

	def start(self):
		resp = self.sendRequest();
		self.handleResponse(resp);

		Utilities.debug("STATUS:");
		Utilities.debug(self.status+" : "+self.result);
		
class WARegRequest(WARequest):
	
	def __init__(self,cc, p_in, code,method="self"):
		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("code",code);
		self.addParam("udid", Utilities.getChatPassword());
		self.addParam("method",method)
		self.base_url = "r.whatsapp.net"
		self.req_file = "/v1/register.php"

	def handleResponse(self,data):
		response_node  = data.getElementsByTagName("response")[0];

		for (name, value) in response_node.attributes.items():
			if name == "login":
				self.login = value

	def start(self):
		resp = self.sendRequest();
		self.handleResponse(resp);

		Utilities.debug("LOGIN:"+self.login);
		

class WAExistsRequest(WARequest):
	
	def __init__(self,cc,p_in):
		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("udid", Utilities.getChatPassword());
		self.base_url = "r.whatsapp.net"
		self.req_file = "/v1/exist.php"


	def handleResponse(self,data):
		response_node  = data.getElementsByTagName("response")[0];

		for (name, value) in response_node.attributes.items():
			if name == "status":
				self.status = value
			elif name == "result":
				self.result = value

	def start(self):
		resp = self.sendRequest();
		self.handleResponse(resp);

		Utilities.debug("STATUS:");
		Utilities.debug(self.status+" : "+self.result);
	

class PhoneRegBase():
	request = None;
	cc = 0;
	number = None;
	smsNumber = None;
	
	def __init__(self):
		self.cc = '20';
		self.number = '1001116688'
		self.smsNumber = self.cc+self.number;
		
	def startCodeRequest(self,method="sms"):
		self.request = WACodeRequest(self.cc,self.number,method);
		self.request.start();
		self.request.onDone();
		
	def startRegRequest(self):
		self.request = WARegRequest(self.cc,self.number,502);
		self.request.start();
		self.request.onDone();
		
	def startExistRequest(self):
		self.request = WAExistsRequest(self.cc,self.number);
		self.request.start();
		self.request.onDone();
		
		

if __name__ == "__main__":
	#reg = PhoneRegBase();
	#reg.startCodeRequest("voice");
	#reg.startExistRequest()
	cc = '20';
	#number = '1001116688'
	#number = '1146068600'
	#number = '1223526683'
	number = '1112442751'
	smsNumber = cc+number;
	code = 565;

	
	c = WACodeRequest(cc,number,'self');
	c.start();
	req = WARegRequest(cc,number,c.result,'self');
	req.start();
	ex = WAExistsRequest(cc,number);
	ex.start();

		
