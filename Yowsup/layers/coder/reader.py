from tokendictionary import TokenDictionary
from barray import ByteArray
from Yowsup import ProtocolTreeNode
import traceback
class Reader:
    def __init__(self, inputstream):

        self.inputKey = None
        self.rawIn = inputstream;
        self.inn = ByteArray();
        self.buf = []#bytearray(1024);
        self.bufSize = 0;
        self.readSize = 1;

        self.tokenDictionary = TokenDictionary()


    def readStanza(self):

        #firstByte = self.readInt8(self.rawIn)
        #stanzaFlag = (firstByte & 0xF0) >> 4
        #stanzaSize = self.readInt16(self.rawIn) | ((firstByte & 0x0F) << 16)


        #isEncrypted = ((stanzaFlag & 8) != 0)

        self.fillBuffer();

        #if self.inputKey is not None and isEncrypted:
            #self.inn.buf = bytearray(self.inn.buf)
        #    self.inn.buf = self.inputKey.decodeMessage(self.inn.buf, 0, 4, len(self.inn.buf)-4)

    def streamStart(self):
        #self.nextTree()
        #return
        self.readStanza();

        tag = self.inn.read();
        size = self.readListSize(tag);
        tag = self.inn.read();


        if tag != 1:
            if tag == 236:
                tag = self.inn.read + 237

            token = self.tokenDictionary.getToken(tag)

            raise Exception("expecting STREAM_START in streamStart, instead got token: %s" % token);
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




    def readString(self,token):

        if token == -1:
            raise Exception("-1 token in readString");

        if token > 2 and token < 245:
            if token == 236:
              token = 237 + self.inn.read()
            return self.tokenDictionary.getToken(token)

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
            return self.tokenMapper.getToken(245+token);
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
        return ret;

    def fillBuffer(self):
        #if len(self.buf) < stanzaSize:
        #   newsize = stanzaSize#max(len(self.buf)*3/2,stanzaSize);

        self.buf = self.rawIn.readAll()#[0 for i in range(0,stanzaSize)]
        #self.bufSize = stanzaSize;
        #self.fillArray(self.buf, stanzaSize, self.rawIn);
        self.inn = ByteArray();
        self.inn.write(self.buf);

        #this.in = new ByteArrayInputStream(this.buf, 0, stanzaSize);
        #self.inn.setReadSize(stanzaSize);
        #Utilities.debug(str(len(self.buf))+":::"+str(stanzaSize));

    def fillArray(self, buf, length, inputstream):
        count = 0;
        while count < length:
            #count+=inputstream.read2(buf,count,length-count);
            buf[count] = inputstream.read();
            count += 1


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

        return ProtocolTreeNode(tag, attribs, None, self.readString(b));

    def readList(self,token):
        size = self.readListSize(token);
        listx = []
        for i in range(0,size):
            listx.append(self.nextTreeInternal());

        return listx;

    def isListTag(self,b):
        return (b == 248) or (b == 0) or (b == 249);