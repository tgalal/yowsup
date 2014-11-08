from .tokendictionary import TokenDictionary
from .barray import ByteArray
class Writer:
    STREAM_START = 1;
    STREAM_END = 2;
    LIST_EMPTY = 0;
    LIST_8 = 248;
    LIST_16 = 249;
    JID_PAIR = 250;
    BINARY_8 = 252;
    BINARY_24 = 253;
    TOKEN_8 = 254;

    def __init__(self, o):
        self.outputKey = None

        self.realOut = o;
        #self.out = o;
        self.tokenMap = {}
        self.out = ByteArray();

        self.tokenDictionary = TokenDictionary()

    def streamStart(self,domain,resource):

        self.realOut.write(87);
        self.realOut.write(65);
        self.realOut.write(1);
        self.realOut.write(4);

        streamOpenAttributes  = {"to":domain,"resource":resource};
        self.writeListStart(len(streamOpenAttributes )*2+1);

        self.out.write(1);

        self.writeAttributes(streamOpenAttributes);
        self.flushBuffer(False);


    def write(self, node,needsFlush = 0):
        if node is None:
            self.out.write(0);
        else:
            self.writeInternal(node);

        self.flushBuffer(needsFlush);
        self.out.buf = [];


    def processBuffer(self):
        self.out.buf = self.out.getBuffer()

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
            key = self.tokenDictionary.getIndex(tag);
            if key > 235:
                self.writeToken(236);
                self.writeToken(key - 237);
            else:
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




