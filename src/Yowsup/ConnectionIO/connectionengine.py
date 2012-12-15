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

import socket;
import sys
from .bintreenode import BinTreeNodeReader, BinTreeNodeWriter

from Yowsup.Common.debugger import Debugger

from .ioexceptions import ConnectionClosedException

class ConnectionEngine(socket.socket):
	
	def __init__(self):
		Debugger.attach(self)

		self.reader = BinTreeNodeReader(self)
		self.writer = BinTreeNodeWriter(self)
		
		self.readSize = 1;
		self.buf = [];
		self.maxBufRead = 0;
		self.connected = 0
		
		self.jid = ""
		
		super(ConnectionEngine,self).__init__(socket.AF_INET, socket.SOCK_STREAM);

	def getId(self):
		return self.id


	def setId(self, idx):
		self.id = idx

	def flush(self):
		'''FLUSH'''
		self.write();
		
	def getBuffer(self):
		return self.buffer;
	
	
	
	def reset(self):
		self.buffer = "";		
	
	def write(self,data):
			
		if type(data) is int:
			try:
				self.sendall(chr(data)) if sys.version_info < (3, 0) else self.sendall(chr(data).encode('iso-8859-1'))
			except:
				self._d("socket 1 write crashed, reason: %s" % sys.exc_info()[1])
				raise ConnectionClosedException("socket 1 write crashed, reason: %s" % sys.exc_info()[1])
		else:
			tmp = "";
			
			for d in data:
				tmp += chr(d)

			try:
				self.sendall(tmp) if sys.version_info < (3, 0) else self.sendall(tmp.encode('iso-8859-1'))
			except:
				self._d("socket 2 write crashed, reason: %s" % sys.exc_info()[1])
				raise ConnectionClosedException("socket 2 write crashed, reason: %s" % sys.exc_info()[1])
		
		
	def setReadSize(self,size):
		self.readSize = size;

		
	def read(self, socketOnly = 0):
		x = ""
		try:
			x = self.recv(self.readSize)#.decode('iso-8859-1');
		except:
			self._d("socket read crashed, reason %s " % sys.exc_info()[1])
			raise ConnectionClosedException("socket read crashed, reason %s " % sys.exc_info()[1])

		#x= self.recvX(self.readSize);
		
		if len(x) == 1:
			#Utilities.debug("GOT "+str(ord((x))));
			return ord(x);
		else:
			raise ConnectionClosedException("Got 0 bytes, connection closed");
			#return x;
		
	def read2(self,b,off,length):
		'''reads into a buffer'''
		if off < 0 or length < 0 or (off+length)>len(b):
			raise Exception("Out of bounds");
		
		if length == 0:
			return 0;
		
		if b is None:
			raise Exception("XNull pointerX");
		
		count = 0;
		
		while count < length:
			
			#self.read();
			#print "OKIIIIIIIIIIII";
			#exit();
			b[off+count]=self.read(0);
			count= count+1;
		
	
		return count;
