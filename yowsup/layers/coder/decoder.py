from yowsup.structs import ProtocolTreeNode
import math
import binascii
import sys
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

    def getToken(self, index, data):
        token = self.tokenDictionary.getToken(index)
        if not token:
            index = self.readInt8(data)
            token = self.tokenDictionary.getToken(index, True)
            if not token:
                raise ValueError("Invalid token %s" % token)

        return token

    def getTokenDouble(self, n, n2):
        pos = n2 + n * 256
        token = self.tokenDictionary.getToken(pos, True)
        if not token:
            raise ValueError("Invalid token %s" % pos)

        return token

    def streamStart(self, data):
        self.streamStarted = True
        tag = data.pop(0)
        size = self.readListSize(tag, data)
        tag = data.pop(0)

        if tag != 1:
            if tag == 236:
                tag = data.pop(0) + 237
            token = self.getToken(tag, data)#self.tokenDictionary.getToken(tag)
            raise Exception("expecting STREAM_START in streamStart, instead got token: %s" % token)
        attribCount = (size - 2 + size % 2) / 2
        self.readAttributes(attribCount, data)

    def readNibble(self, data):
        _byte = self.readInt8(data)
        ignoreLastNibble = bool(_byte & 0x80)
        size = (_byte & 0x7f)
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

    def readPacked8(self, n, data):
        size = self.readInt8(data)
        remove = 0
        if (size & 0x80) != 0 and n == 251:
            remove = 1
        size = size & 0x7F
        text = bytearray(self.readArray(size, data))
        hexData = binascii.hexlify(str(text) if sys.version_info < (2,7) else text).upper()
        dataSize = len(hexData)
        out = []
        if remove == 0:
            for i in range(0, dataSize):
                char = chr(hexData[i]) if type(hexData[i]) is int else hexData[i] #python2/3 compat
                val = ord(binascii.unhexlify("0%s" % char))
                if i == (dataSize - 1) and val > 11 and n != 251: continue
                out.append(self.unpackByte(n, val))
        else:
            out =  map(ord, list(hexData[0: -remove])) if sys.version_info < (3,0) else list(hexData[0: -remove])

        return out

    def unpackByte(self, n, n2):
        if n == 251:
            return self.unpackHex(n2)
        if n == 255:
            return self.unpackNibble(n2)
        raise ValueError("bad packed type %s" % n)

    def unpackHex(self, n):
        if n in range(0, 10):
            return n + 48
        if n in range(10, 16):
            return 65 + (n - 10)

        raise ValueError("bad hex %s" % n)

    def unpackNibble(self, n):
        if n in range(0, 10):
            return n + 48
        if n in (10, 11):
            return 45 + (n - 10)
        raise ValueError("bad nibble %s" % n)


    def readHeader(self, data, offset = 0):
        ret = 0
        if len(data) >= (3 + offset):
            b0 = data[offset]
            b1 = data[offset + 1]
            b2 = data[offset + 2]
            ret = b0 + (b1 << 16) + (b2 << 8)

        return ret

    def readInt8(self, data):
        return data.pop(0);

    def readInt16(self, data):
        intTop = data.pop(0)
        intBot = data.pop(0)
        value = (intTop << 8) + intBot
        if value is not None:
            return value
        else:
            return ""

    def readInt20(self, data):
         int1 = data.pop(0)
         int2 = data.pop(0)
         int3 = data.pop(0)
         return ((int1 & 0xF) << 16) | (int2 << 8) | int3

    def readInt24(self, data):
        int1 = data.pop(0)
        int2 = data.pop(0)
        int3 = data.pop(0)
        value = (int1 << 16) + (int2 << 8) + (int3 << 0)
        return value

    def readInt31(self, data):
        data.pop(0)
        int1 = data.pop(0)
        int2 = data.pop(0)
        int3 = data.pop(0)
        return (int1 << 24) | (int1 << 16) | int2 << 8 | int3

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
            key = self.readString(self.readInt8(data), data)
            value = self.readString(self.readInt8(data), data)
            attribs[key]=value
        return attribs

    def readString(self,token, data):
        if token == -1:
            raise Exception("-1 token in readString")

        if 2 < token < 236:
            return self.getToken(token, data)

        if token == 0:
            return None

        if token in (236, 237, 238, 239):
            return self.getTokenDouble(token - 236, self.readInt8(data))

        if token == 250:
            user = self.readString(data.pop(0), data)
            server = self.readString(data.pop(0), data)
            if user is not None and server is not None:
                return user + "@" + server
            if server is not None:
                return server
            raise Exception("readString couldn't reconstruct jid")

        if token in (251, 255):
            return "".join(map(chr, self.readPacked8(token, data)))

        if token == 252:
            size8 = self.readInt8(data)
            buf8 = self.readArray(size8, data)
            return "".join(map(chr, buf8))

        if token == 253:
            size20 = self.readInt20(data)
            buf20 = self.readArray(size20, data)
            return "".join(map(chr, buf20))

        if token == 254:
            size31 = self.readInt31()
            buf31 = self.readArray(size31, data)
            return "".join(map(chr, buf31))


        raise Exception("readString couldn't match token "+str(token))

    def readArray(self, length, data):
        out = []
        for i in range(0, length):
            out.append(data.pop(0))

        return out

    def nextTreeInternal(self, data):
        size = self.readListSize(self.readInt8(data), data)
        token = self.readInt8(data)
        if token == 1:
            token = self.readInt8(data)

        if token == 2:
            return None

        tag = self.readString(token, data)

        if size == 0 or tag is None:
            raise ValueError("nextTree sees 0 list or null tag")

        attribCount = (size - 2 + size % 2)/2
        attribs = self.readAttributes(attribCount, data)
        if size % 2 ==1:
            return ProtocolTreeNode(tag, attribs)

        read2 = self.readInt8(data)

        nodeData = None
        nodeChildren = None
        if self.isListTag(read2):
            nodeChildren = self.readList(read2, data)
        elif read2 == 252:
            size = self.readInt8(data)
            nodeData = self.readArray(size, data)
        elif read2 == 253:
            size = self.readInt20(data)
            nodeData = self.readArray(size, data)
        elif read2 == 254:
            size = self.readInt31(data)
            nodeData = self.readArray(size, data)
        elif read2 in (255, 251):
            nodeData = self.readPacked8(read2, data)
        else:
            nodeData = self.readString(read2, data)

        if nodeData and type(nodeData) is not str:
            nodeData = "".join(map(chr, nodeData))

        return ProtocolTreeNode(tag, attribs, nodeChildren, nodeData)

    def readList(self,token, data):
        size = self.readListSize(token, data)
        listx = []
        for i in range(0,size):
            listx.append(self.nextTreeInternal(data))

        return listx;

    def isListTag(self, b):
        return b in (248, 0, 249)
