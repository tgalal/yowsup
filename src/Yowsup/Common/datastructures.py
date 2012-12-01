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


class ByteArray():
	def __init__(self,size=0):
		self.size = size;
		self.buf = [0] * size#bytearray(size);

	def toByteArray(self):
		res = ByteArray();
		for b in self.buf:
			res.buf.append(b);

		return res;

	def reset(self):
		self.buf = [0] * self.size;

	def getBuffer(self):
		return self.buf

	def read(self):
		return self.buf.pop(0);

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
			b[off+count]=self.read();
			count= count+1;


		return count;

	def write(self,data):
		if type(data) is int:
			self.writeInt(data);
		elif type(data) is chr:
			self.buf.append(ord(data));
		elif type(data) is str:
			self.writeString(data);
		elif type(data) is list:
			self.writeByteArray(data);
		else:
			raise Exception("Unsupported datatype "+str(type(data)));

	def writeByteArray(self,b):
		for i in b:
			self.buf.append(i);

	def writeInt(self,integer):
		self.buf.append(integer);

	def writeString(self,string):
		for c in string:
			self.writeChar(c);

	def writeChar(self,char):
		self.buf.append(ord(char))

