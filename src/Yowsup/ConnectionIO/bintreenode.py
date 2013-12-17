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
from Yowsup.Common.datastructures import ByteArray
from Yowsup.Common.constants import Constants


from .protocoltreenode import ProtocolTreeNode
from .ioexceptions import InvalidReadException

class BinTreeNodeReader():
    def __init__(self,inputstream):
        
        Debugger.attach(self)

        self.inputKey = None
        
        self._d('Reader init');
        self.tokenMap = Constants.dictionary;
        self.rawIn = inputstream;
        self.inn = ByteArray();
        self.buf = []#bytearray(1024);
        self.bufSize = 0;
        self.readSize = 1;
        

    def readStanza(self):

        num = self.readInt8(self.rawIn)
        stanzaSize = self.readInt16(self.rawIn,1);

        header = (num << 16) + stanzaSize#self.readInt24(self.rawIn)
        
        flags = (header >> 20);
        #stanzaSize =  ((header & 0xF0000) >> 16) | ((header & 0xFF00) >> 8) | (header & 0xFF);
        isEncrypted = ((flags & 8) != 0)
        
        self.fillBuffer(stanzaSize);
        
        if self.inputKey is not None and isEncrypted:
            #self.inn.buf = bytearray(self.inn.buf)
            self.inn.buf = self.inputKey.decodeMessage(self.inn.buf, 0, 4, len(self.inn.buf)-4)[4:]

    def streamStart(self):

        self.readStanza();
        
        tag = self.inn.read();
        size = self.readListSize(tag);
        tag = self.inn.read();
        if tag != 1:
            raise Exception("expecting STREAM_START in streamStart");
        attribCount = (size - 2 + size % 2) / 2;
        self.readAttributes(attribCount);
    
    def readInt8(self,i):
        return i.read();
        
    def readInt16(self,i,socketOnly=0):
        intTop = i.read(socketOnly);
        intBot = i.read(socketOnly);
        #Utilities.debug(str(intTop)+"------------"+str(intBot));
        value = (intTop << 8) + intBot;
        if value is not None:
            return value;
        else:
            return "";
    
    
    def readInt24(self,i):
        int1 = i.read();
        int2 = i.read();
        int3 = i.read();
        value = (int1 << 16) + (int2 << 8) + (int3 << 0);
        return value;
        

    
    def readListSize(self,token):
        size = 0;
        if token == 0:
            size = 0;
        else:
            if token == 248:
                size = self.readInt8(self.inn);
            else:
                if token == 249:
                    size = self.readInt16(self.inn);
                else:
                    #size = self.readInt8(self.inn);
                    raise Exception("invalid list size in readListSize: token " + str(token));
        return size;
    
    def readAttributes(self,attribCount):
        attribs = {};
        
        for i in range(0, int(attribCount)):
            key = self.readString(self.inn.read());
            value = self.readString(self.inn.read());
            attribs[key]=value;
        return attribs;
    
    def getToken(self,token):
        if (token >= 0 and token < len(self.tokenMap)):
            ret = self.tokenMap[token];
        else:
            raise Exception("invalid token/length in getToken %i "%token);
        
        return ret;
        
    
    def readString(self,token):
        
        if token == -1:
            raise Exception("-1 token in readString");
        
        if token > 4 and token < 245:
            return self.getToken(token);
        
        if token == 0:
            return None;
            

        if token == 252:
            size8 = self.readInt8(self.inn);
            buf8 = [0] * size8;
            
            self.fillArray(buf8,len(buf8),self.inn);
            #print self.inn.buf;
            return "".join(map(chr, buf8));
            #return size8;
            
        
        if token == 253:
            size24 = self.readInt24(self.inn);
            buf24 = [0] * size24;
            self.fillArray(buf24,len(buf24),self.inn);
            return "".join(map(chr, buf24));
            
        if token == 254:
            token = self.inn.read();
            return self.getToken(245+token);
        if token == 250:
            user = self.readString(self.inn.read());
            server = self.readString(self.inn.read());
            if user is not None and server is not None:
                return user + "@" + server;
            if server is not None:
                return server;
            raise Exception("readString couldn't reconstruct jid");
        
        raise Exception("readString couldn't match token "+str(token));
        
    def nextTree(self):
        self.inn.buf = [];
        
        self.readStanza();
        
        ret = self.nextTreeInternal();
        self._d("Incoming")
        if ret is not None:
            if '<picture type="' in ret.toString():
                self._d("<Picture!!!>");
            else:
                self._d("\n%s"%ret.toString());
        return ret;
    
    def fillBuffer(self,stanzaSize):
        #if len(self.buf) < stanzaSize:
        #   newsize = stanzaSize#max(len(self.buf)*3/2,stanzaSize);

        self.buf = [0 for i in range(0,stanzaSize)]
        self.bufSize = stanzaSize;
        self.fillArray(self.buf, stanzaSize, self.rawIn);
        self.inn = ByteArray();
        self.inn.write(self.buf);
        
        #this.in = new ByteArrayInputStream(this.buf, 0, stanzaSize);
        #self.inn.setReadSize(stanzaSize);
        #Utilities.debug(str(len(self.buf))+":::"+str(stanzaSize));
    
    def fillArray(self, buf,length,inputstream):
        count = 0;
        while count < length:
            count+=inputstream.read2(buf,count,length-count);

    def nextTreeInternal(self):
        
        b = self.inn.read();
        
        size = self.readListSize(b);
        b = self.inn.read();
        if b == 2:
            return None;
        
        
        tag = self.readString(b);
        if size == 0 or tag is None:
            raise InvalidReadException("nextTree sees 0 list or null tag");
        
        attribCount = (size - 2 + size%2)/2;
        attribs = self.readAttributes(attribCount);
        if size % 2 ==1:
            return ProtocolTreeNode(tag,attribs);
            
        b = self.inn.read();

        if self.isListTag(b):
            return ProtocolTreeNode(tag,attribs,self.readList(b));
        
        return ProtocolTreeNode(tag,attribs,None,self.readString(b));
        
    def readList(self,token):
        size = self.readListSize(token);
        listx = []
        for i in range(0,size):
            listx.append(self.nextTreeInternal());
        
        return listx;    
        
    def isListTag(self,b):
        return (b == 248) or (b == 0) or (b == 249);



class BinTreeNodeWriter():
    STREAM_START = 1;
    STREAM_END = 2;
    LIST_EMPTY = 0;
    LIST_8 = 248;
    LIST_16 = 249;
    JID_PAIR = 250;
    BINARY_8 = 252;
    BINARY_24 = 253;
    TOKEN_8 = 254;
    #socket out; #FunXMPP.WAByteArrayOutputStream
    #socket realOut;
    tokenMap={}
    
    def __init__(self,o):
        Debugger.attach(self)

        self.outputKey = None

        dictionary = Constants.dictionary
        self.realOut = o;
        #self.out = o;
        self.tokenMap = {}
        self.out = ByteArray();
        #this.tokenMap = new Hashtable(dictionary.length);
        for i in range(0,len(dictionary)):
            if dictionary[i] is not None:
                self.tokenMap[dictionary[i]]=i
        
        #Utilities.debug(self.tokenMap);
        '''
        for (int i = 0; i < dictionary.length; i++)
            if (dictionary[i] != null)
                this.tokenMap.put(dictionary[i], new Integer(i));
        '''

    def streamStart(self,domain,resource):
        
        self.realOut.write(87);
        self.realOut.write(65);
        self.realOut.write(1);
        self.realOut.write(2);

        streamOpenAttributes  = {"to":domain,"resource":resource};
        self.writeListStart(len(streamOpenAttributes )*2+1);

        self.out.write(1);

        self.writeAttributes(streamOpenAttributes);
        self.flushBuffer(False);


    def write(self, node,needsFlush = 0):
        if node is None:
            self.out.write(0);
        else:
            self._d("Outgoing");
            self._d("\n %s" % node.toString());
            self.writeInternal(node);

        self.flushBuffer(needsFlush);
        self.out.buf = [];


    def processBuffer(self):
        buf = self.out.getBuffer()

        prep = [0,0,0]
        prep.extend(buf)

        length1 = len(self.out.buf)
        num = 0

        if self.outputKey is not None:
            num = 1
            prep.extend([0,0,0,0])
            length1 += 4

            #prep = bytearray(prep)
            res = self.outputKey.encodeMessage(prep, len(prep) - 4 , 3, len(prep)-4-3)

            res[0] = ((num << 4) | (length1 & 16711680) >> 16) % 256
            res[1] = ((length1 & 65280) >> 8) % 256
            res[2] = (length1 & 255) % 256

            self.out.buf = res

            return
        else:
            prep[0] = ((num << 4) | (length1 & 16711680) >> 16) % 256
            prep[1] = ((length1 & 65280) >> 8) % 256
            prep[2] = (length1 & 255) % 256
            self.out.buf = prep

    def flushBuffer(self, flushNetwork):
        '''define flush buffer here '''
        self.processBuffer()

        size = len(self.out.getBuffer());
        if (size & 0xFFFFF) != size:
            raise Exception("Buffer too large: "+str(size));

        #self.realOut.write(0)
        #self.writeInt16(size,self.realOut);


        self.realOut.write(self.out.getBuffer());
        self.out.reset();

        if flushNetwork:
            self.realOut.flush();

    def writeInternal(self,node):
        '''define write internal here'''
        
        x = 1 + (0 if node.attributes is None else len(node.attributes) * 2) + (0 if node.children is None else 1) + (0 if node.data is None else 1);
    
        self.writeListStart(1 + (0 if node.attributes is None else len(node.attributes) * 2) + (0 if node.children is None else 1) + (0 if node.data is None else 1));
        
        self.writeString(node.tag);
        self.writeAttributes(node.attributes);
        
        if node.data is not None:
            self.writeBytes(node.data)
            '''if type(node.data) == bytearray:
                self.writeBytes(node.data);
            else:
                self.writeBytes(bytearray(node.data));
            '''
        
        if node.children is not None:
            self.writeListStart(len(node.children));
            for c in node.children:
                self.writeInternal(c);
    
    
    def writeAttributes(self,attributes):
        if attributes is not None:
            for key, value in attributes.items():
                self.writeString(key);
                self.writeString(value);
        
        
    def writeBytes(self,bytes):

        length = len(bytes);
        if length >= 256:
            self.out.write(253);
            self.writeInt24(length);
        else:
            self.out.write(252);
            self.writeInt8(length);
            
        for b in bytes:
            self.out.write(b);
        
    def writeInt8(self,v):
        self.out.write(v & 0xFF);

    
    def writeInt16(self,v, o = None):
        if o is None:
            o = self.out;

        o.write((v & 0xFF00) >> 8);
        o.write((v & 0xFF) >> 0);

    
    def writeInt24(self,v):
        self.out.write((v & 0xFF0000) >> 16);
        self.out.write((v & 0xFF00) >> 8);
        self.out.write((v & 0xFF) >> 0);
    

    def writeListStart(self,i):
        #Utilities.debug("list start "+str(i));
        if i == 0:
            self.out.write(0)
        elif i < 256:
            self.out.write(248);
            self.writeInt8(i);#f
        else:
            self.out.write(249);
            #write(i >> 8 & 0xFF);
            self.writeInt16(i); #write(i >> 8 & 0xFF);
        
    def writeToken(self, intValue):
        if intValue < 245:
            self.out.write(intValue)
        elif intValue <=500:
            self.out.write(254)
            self.out.write(intValue - 245);
    
    def writeString(self,tag):
        try:
            key = self.tokenMap[tag];
            self.writeToken(key);
        except KeyError:
            try:

                at = '@'.encode() if type(tag) == bytes else '@'
                atIndex = tag.index(at);

                if atIndex < 1:
                    raise ValueError("atIndex < 1");
                else:
                    server = tag[atIndex+1:];
                    user = tag[0:atIndex];
                    #Utilities.debug("GOT "+user+"@"+server);
                    self.writeJid(user, server);

            except ValueError:
                self.writeBytes(self.encodeString(tag));

    def encodeString(self, string):
        res = [];
        
        if type(string) == bytes:
            for char in string:
                res.append(char)
        else:
            for char in string:
                res.append(ord(char))
        return res;
    
    def writeJid(self,user,server):
        self.out.write(250);
        if user is not None:
            self.writeString(user);
        else:
            self.writeToken(0);
        self.writeString(server);

        
    def getChild(self,string):
        if self.children is None:
            return None
        
        for c in self.children:
            if string == c.tag:
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
 
