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


import base64, random;
import os,binascii
import socket
from Tools.debugger import Debugger
import hashlib
from ConnectionIO.protocoltreenode import ProtocolTreeNode

class DigestAuth():

	def __init__(self,conn):
		Debugger.attach(self);

		self.conn = conn
		self._d("Yowsup DigestAuth INIT");

	def setAuthObject(self, authObject):
		self.authObject = authObject
	
	def login(self, username, password, domain, resource):

		try:
			self._d("Starting stream")
			self.conn.writer.streamStart(domain,resource);

			self._d("Sending Features")
			self.sendFeatures();

			self._d("Sending Auth");
			self.sendAuth();

			self._d("Read stream start");
			self.conn.reader.streamStart();

			self._d("Read features and challenge");
			challengeData = self.readFeaturesAndChallenge();
			
			self._d("Sending Response")
			self.sendResponse(challengeData);

			self._d("Read success")
			self.readSuccess();
			
			self.conn.jid = "%s@%s" % (username, domain)
			return self.conn

		except socket.error:
			return self.connectionError.emit()


	def sendFeatures(self):
		toWrite = ProtocolTreeNode("stream:features",None,[ ProtocolTreeNode("receipt_acks",None,None),ProtocolTreeNode("w:profile:picture",{"type":"all"},None), ProtocolTreeNode("w:profile:picture",{"type":"group"},None),ProtocolTreeNode("notification",{"type":"participant"},None), ProtocolTreeNode("status",None,None) ]);
		self.conn.writer.write(toWrite);

	def sendAuth(self):
		# "user":self.connection.user,
		node = ProtocolTreeNode("auth",{"xmlns":"urn:ietf:params:xml:ns:xmpp-sasl","mechanism":"DIGEST-MD5-1"});
		self.conn.writer.write(node);

	def readFeaturesAndChallenge(self):
		server_supports_receipt_acks = True;
		root = self.conn.reader.nextTree();

		while root is not None:
			if ProtocolTreeNode.tagEquals(root,"stream:features"):
				self._d("GOT FEATURES !!!!");
				self.authObject.supportsReceiptAcks  = root.getChild("receipt_acks") is not None;
				root = self.conn.reader.nextTree();

				continue;

			if ProtocolTreeNode.tagEquals(root,"challenge"):
				self._d("GOT CHALLENGE !!!!");
				data = base64.b64decode(root.data);
				return data;
		raise Exception("fell out of loop in readFeaturesAndChallenge");


	def sendResponse(self,challengeData):

		response = self.getResponse(challengeData);
		node = ProtocolTreeNode("response",{"xmlns":"urn:ietf:params:xml:ns:xmpp-sasl"}, None, str(base64.b64encode(response)));
		self.conn.writer.write(node);
		self.conn.reader.inn.buf = [];

	def getResponse(self,challenge):
		self._d(str(challenge))
		nonce_key = "nonce=\""
		i = challenge.index(nonce_key);

		i+=len(nonce_key);
		j = challenge.index('"',i);

		nonce = challenge[i:j];
		
		cnonce = binascii.b2a_hex(os.urandom(6))

		nc = "00000001";
		bos = bytearray();
		bos.extend(hashlib.md5(self.authObject.username + ":" + self.authObject.domain + ":" + self.authObject.password).digest());
		bos.append(58);
		bos.extend(nonce);
		bos.append(58);
		bos.extend(cnonce);

		digest_uri = "xmpp/"+self.authObject.domain;

		A1 = buffer(bos)
		A2 = "AUTHENTICATE:" + digest_uri;

		KD = hashlib.md5(A1).hexdigest() + ":"+nonce+":"+nc+":"+cnonce+":auth:"+ hashlib.md5(A2).hexdigest();

		response = hashlib.md5(KD).hexdigest();
		bigger_response = "";
		bigger_response += "realm=\"";
		bigger_response += self.authObject.domain
		bigger_response += "\",response=";
		bigger_response += response
		bigger_response += ",nonce=\"";
		bigger_response += nonce
		bigger_response += "\",digest-uri=\""
		bigger_response += digest_uri
		bigger_response += "\",cnonce=\""
		bigger_response += cnonce
		bigger_response += "\",qop=auth";
		bigger_response += ",username=\""
		bigger_response += self.authObject.username
		bigger_response += "\",nc="
		bigger_response += nc

		self._d(str(bigger_response))
		return bigger_response;

	def readSuccess(self):
		node = self.conn.reader.nextTree();
		self._d("Login Status: %s"%(node.tag));

		if ProtocolTreeNode.tagEquals(node,"failure"):
			self.authObject.authenticationFailed()
			raise Exception("Login Failure");

		ProtocolTreeNode.require(node,"success");

		expiration = node.getAttributeValue("expiration");

		if expiration is not None:
			self._d("Expires: "+str(expiration));
			self.authObject.expireDate = expiration;

		kind = node.getAttributeValue("kind");
		self._d("Account type: %s"%(kind))

		if kind == "paid":
			self.authObject.accountKind = 1;
		elif kind == "free":
			self.authObject.accountKind = 0;
		else:
			self.authObject.accountKind = -1;

		status = node.getAttributeValue("status");
		self._d("Account status: %s"%(status));

		if status == "expired":
			self.loginFailed.emit()
			raise Exception("Account expired on "+str(self.authObject.expireDate));

		if status == "active":
			if expiration is None:
				#raise Exception ("active account with no expiration");
				'''@@TODO expiration changed to creation'''
		else:
			self.authObject.accountKind = 1;

		self.conn.reader.inn.buf = [];

		self.authObject.authenticationComplete()