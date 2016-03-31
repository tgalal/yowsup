from yowsup.structs import ProtocolTreeNode
import math
class ReadDecoder:
    def __init__(self, tokenDictionary):
        self.streamStarted = False;
        self.tokenDictionary = tokenDictionary

    def reset(self):
        self.streamStarted = False

    def getProtocolTreeNode(self, data):
        if not self.streamStarted:
            return self.streamStart(data)
        return self.nextTreeInternal(data)

    def _getToken(self, index, data):
        token = self.tokenDictionary.getToken(index)
        if not token:
            index = self.readInt8(data)
            token = self.tokenDictionary.getToken(index, True)
            if not token:
                raise ValueError("Invalid token %s" % token)

        return token

    def streamStart(self, data):
        self.streamStarted = True
        tag = data.pop(0)
        size = self.readListSize(tag, data)
        tag = data.pop(0)

        if tag != 1:
            if tag == 236:
                tag = data.pop(0) + 237
            token = self._getToken(tag, data)#self.tokenDictionary.getToken(tag)
            raise Exception("expecting STREAM_START in streamStart, instead got token: %s" % token)
        attribCount = (size - 2 + size % 2) / 2
        self.readAttributes(attribCount, data)

    def readNibble(self, data):
        _byte = self.readInt8(data)
        ignoreLastNibble = bool(_byte & 0x80)
        size = (_byte & 0x7f);
        nrOfNibbles = size * 2 - int(ignoreLastNibble)
        dataArr = self.readArray(size, data)
        string = ''
        for i in range(0, nrOfNibbles):
            _byte = dataArr[int(math.floor(i/2))]
            _shift = 4 * (1 - i % 2)
            dec = (_byte & (15 << _shift)) >> _shift

            if dec in (0,1,2,3,4,5,6,7,8,9):
                string += str(dec)
            elif dec in (10, 11):
                string += chr(dec - 10 + 45)
            else:
                raise Exception("Bad nibble %s" % dec)
        return string





    def readInt8(self,data):
        return data.pop(0);

    def readInt16(self, data):
        intTop = data.pop(0)
        intBot = data.pop(0)
        value = (intTop << 8) + intBot
        if value is not None:
            return value
        else:
            return ""

    def readInt24(self,data):
        int1 = data.pop(0)
        int2 = data.pop(0)
        int3 = data.pop(0)
        value = (int1 << 16) + (int2 << 8) + (int3 << 0)
        return value


    def readListSize(self,token, data):
        size = 0
        if token == 0:
            size = 0
        else:
            if token == 248:
                size = self.readInt8(data)
            else:
                if token == 249:
                    size = self.readInt16(data)
                else:
                    raise Exception("invalid list size in readListSize: token " + str(token))
        return size

    def readAttributes(self, attribCount, data):
        attribs = {}

        for i in range(0, int(attribCount)):
            key = self.readString(data.pop(0), data)
            value = self.readString(data.pop(0), data)
            attribs[key]=value
        return attribs


    def readString(self,token, data):

        if token == -1:
            raise Exception("-1 token in readString")

        if token > 2 and token < 245:
            return self._getToken(token, data)

        if token == 0:
            return None


        if token == 252:
            size8 = self.readInt8(data)
            buf8 = self.readArray(size8, data)
            return "".join(map(chr, buf8))


        if token == 253:
            size24 = self.readInt24(data)
            buf24 = self.readArray(size24, data)
            return "".join(map(chr, buf24))

        if token == 250:
            user = self.readString(data.pop(0), data)
            server = self.readString(data.pop(0), data)
            if user is not None and server is not None:
                return user + "@" + server
            if server is not None:
                return server
            raise Exception("readString couldn't reconstruct jid")
        elif token == 255:
            return self.readNibble(data)

        raise Exception("readString couldn't match token "+str(token))

    def readArray(self, length, data):
        out = []
        for i in range(0, length):
            out.append(data.pop(0))

        return out

    def nextTreeInternal(self, data):
        b = data.pop(0)

        size = self.readListSize(b, data)
        b = data.pop(0)
        if b == 2:
            return None


        tag = self.readString(b, data)
        if size == 0 or tag is None:
            raise ValueError("nextTree sees 0 list or null tag")

        attribCount = (size - 2 + size % 2)/2;
        attribs = self.readAttributes(attribCount, data)
        if size % 2 ==1:
            return ProtocolTreeNode(tag, attribs)

        b = data.pop(0)

        if self.isListTag(b):
            return ProtocolTreeNode(tag,attribs,self.readList(b, data))

        return ProtocolTreeNode(tag, attribs, None, self.readString(b, data))

    def readList(self,token, data):
        size = self.readListSize(token, data)
        listx = []
        for i in range(0,size):
            listx.append(self.nextTreeInternal(data))

        return listx;

    def isListTag(self, b):
        return b in (248, 0, 249)
