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

from Yowsup.Common.debugger import Debugger


class ProtocolTreeNode():
	
	def __init__(self,tag,attributes,children=None,data=None):

		Debugger.attach(self)

		self.tag = tag;
		self.attributes = attributes;
		self.children = children;
		self.data = data

	def toString(self, depth = 0):
		try:
			out = (" " * depth) + "<"+self.tag;
			if self.attributes is not None:
				for key,val in self.attributes.items():
					out+= " "+key+'="'+val+'"'
			out+= ">\n";
			if self.data is not None:
				out += (" " * (depth + 4)) + self.data.encode("hex") + "\n"

			if self.children is not None:
				for c in self.children:
					out+=c.toString(depth + 4);
			#print sel
			out+= (" " * depth) + "</"+self.tag+">\n"
			return out
		except TypeError:
			print("ignored toString call, probably encountered byte")
		except UnicodeDecodeError:
			print("ingnored toString call, encountered unicode error")
		
		
	
	@staticmethod	
	def tagEquals(node,string):
		return node is not None and node.tag is not None and node.tag == string;
		
		
	@staticmethod
	def require(node,string):
		if not ProtocolTreeNode.tagEquals(node,string):
			raise Exception("failed require. string: "+string);
	
	
	def getChild(self,identifier):

		if self.children is None or len(self.children) == 0:
			return None
		if type(identifier) == int:
			if len(self.children) > identifier:
				return self.children[identifier]
			else:
				return None

		for c in self.children:
			if identifier == c.tag:
				return c;

		return None;
		
	def getAttributeValue(self,string):
		
		if self.attributes is None:
			return None;
		
		try:
			val = self.attributes[string]
			return val;
		except KeyError:
			return None;

	def getAllChildren(self,tag = None):
		ret = [];
		if self.children is None:
			return ret;
			
		if tag is None:
			return self.children
		
		for c in self.children:
			if tag == c.tag:
				ret.append(c)
		
		return ret;

		
	
