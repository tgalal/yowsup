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
from xml.dom import minidom

class WARegRequest(WARequest):
	
	def __init__(self,cc, p_in, code, password):
		self.addParam("cc",cc);
		self.addParam("in",p_in);
		self.addParam("code",code);
		self.addParam("udid", password);
		#self.addParam("method",method)
		self.base_url = "r.whatsapp.net"
		self.req_file = "/v1/register.php"
		
		self.login=0
		super(WARegRequest,self).__init__();

	def handleResponse(self,data):
		response_node  = data.getElementsByTagName("response")[0];

		for (name, value) in response_node.attributes.items():
			if name == "login":
				self.login = value
			
			if name == "status":
				self.status = value

	def register(self):
		resp = self.sendRequest();
		self.handleResponse(minidom.parseString(resp));
		return [self.status, self.login]