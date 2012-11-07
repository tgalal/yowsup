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

from warequest import WARequest
import hashlib
from xml.dom import minidom

class WACodeRequest(WARequest):
	def __init__(self,cc, p_in, method="sms"):
		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("to",cc+p_in);
		self.addParam("lc","US");
		self.addParam("lg","en");
		self.addParam("mcc","000");
		self.addParam("mnc","000");
		self.addParam("imsi","000000000000000");
		self.addParam("method",method);

		token = "k7Iy3bWARdNeSL8gYgY6WveX12A1g4uTNXrRzt1H"+"889d4f44e479e6c38b4a834c6d8417815f999abe"+p_in
		digest = hashlib.md5(token)
		self.addParam("token", digest.hexdigest())

		self.base_url = "r.whatsapp.net"
		self.req_file = "/v1/code.php"
		super(WACodeRequest,self).__init__();
		
	def handleResponse(self,data):
		response_node  = data.getElementsByTagName("response")[0];

		for (name, value) in response_node.attributes.items():
			if name == "status":
				self.status = value
			elif name == "result":
				self.result = value

	def requestCode(self):
		resp = self.sendRequest();
		resp = minidom.parseString(resp)
		self.handleResponse(resp);
		return [self.status, self.result]
