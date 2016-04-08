class WriteEncoder:

    def __init__(self, tokenDictionary):
        self.tokenDictionary = tokenDictionary
        self.streamStarted = False

    def reset(self):
        self.streamStarted = False

    def getStreamStartBytes(self, domain, resource):
        data = []
        self.streamStarted = True
        data.append(87)
        data.append(65)
        data.append(1)
        data.append(6)

        streamOpenAttributes = {"to": domain, "resource": resource}
        self.writeListStart(len(streamOpenAttributes) * 2 + 1, data)
        data.append(1);
        self.writeAttributes(streamOpenAttributes, data)
        return data

    def protocolTreeNodeToBytes(self, node):
        outBytes = []
        self.writeInternal(node, outBytes)

        return outBytes


    def writeInternal(self, node, data):

        x = 1 + \
        (0 if node.attributes is None else len(node.attributes) * 2) + \
        (0 if not node.hasChildren() else 1) + \
        (0 if node.data is None else 1)

        self.writeListStart(x, data)


        self.writeString(node.tag, data)
        self.writeAttributes(node.attributes, data);


        if node.data is not None:
            self.writeBytes(node.data, data)

        if node.hasChildren():
            self.writeListStart(len(node.children), data);
            for c in node.children:
                self.writeInternal(c, data);


    def writeAttributes(self, attributes, data):
        if attributes is not None:
            for key, value in attributes.items():
                self.writeString(key, data);
                self.writeString(value, data, True);


    def writeBytes(self, bytes_, data, packed = False):
        bytes__ = []
        for b in bytes_:
            if type(b) is int:
                bytes__.append(b)
            else:
                bytes__.append(ord(b))


        size = len(bytes__)
        toWrite = bytes__
        if size >= 0x100000:
            data.append(254)
            self.writeInt31(size, data)
        elif size >= 0x100:
            data.append(253)
            self.writeInt20(size, data)
        else:
            r = None
            if packed:
                if size < 128:
                    r = self.tryPackAndWriteHeader(255, bytes__, data)
                    if r is None:
                        r = self.tryPackAndWriteHeader(251, bytes__, data)

            if r is None:
                data.append(252)
                self.writeInt8(size, data)
            else:
                toWrite = r

        data.extend(toWrite)

    def writeInt8(self, v, data):
        data.append(v & 0xFF)


    def writeInt16(self, v, data):
        data.append((v & 0xFF00) >> 8);
        data.append((v & 0xFF) >> 0);

    def writeInt20(self, v, data):
        data.append((0xF0000 & v) >> 16)
        data.append((0xFF00 & v) >> 8)
        data.append((v & 0xFF) >> 0)

    def writeInt24(self, v, data):
        data.append((v & 0xFF0000) >> 16)
        data.append((v & 0xFF00) >> 8)
        data.append((v & 0xFF) >> 0)

    def writeInt31(self, v, data):
        data.append((0x7F000000 & v) >> 24)
        data.append((0xFF0000 & v) >> 16)
        data.append((0xFF00 & v) >> 8)
        data.append((v & 0xFF) >> 0)

    def writeListStart(self, i, data):
        if i == 0:
            data.append(0)
        elif i < 256:
            data.append(248)
            self.writeInt8(i, data)
        else:
            data.append(249)
            self.writeInt16(i, data)

    def writeToken(self, token, data):
        if token <= 255 and token >=0:
            data.append(token)
        else:
            raise ValueError("Invalid token: %s" % token)


    def writeString(self, tag, data, packed = False):
        tok = self.tokenDictionary.getIndex(tag)
        if tok:
            index, secondary = tok
            if secondary:
                self.writeToken(236, data)
            self.writeToken(index, data)
        else:
            at = '@'.encode() if type(tag) == bytes else '@'
            try:
                atIndex = tag.index(at)

                if atIndex < 1:
                    raise ValueError("atIndex < 1")
                else:
                    server = tag[atIndex+1:]
                    user = tag[0:atIndex]
                    self.writeJid(user, server, data)
            except ValueError:
                self.writeBytes(self.encodeString(tag), data, packed)

    def encodeString(self, string):
        res = []

        if type(string) == bytes:
            for char in string:
                res.append(char)
        else:
            for char in string:
                res.append(ord(char))
        return res;

    def writeJid(self, user, server, data):
        data.append(250)
        if user is not None:
            self.writeString(user, data, True)
        else:
            self.writeToken(0, data)
        self.writeString(server, data)


    def tryPackAndWriteHeader(self, v, headerData, data):
        size = len(headerData)
        if size >= 128:
            return None

        arr = [0] * int((size + 1) / 2)
        for i in range(0, size):
            packByte = self.packByte(v, headerData[i])
            if packByte == -1:
                arr = []
                break
            n2 = int(i / 2)
            arr[n2] |= (packByte << 4 * (1 - i % 2))
        if len(arr) > 0:
            if size % 2 == 1:
                arr[-1] |= 15 #0xF
            data.append(v)
            self.writeInt8(size %2 << 7 | len(arr), data)
            return arr

        return None



    def packByte(self, v, n2):
        if v == 251:
            return self.packHex(n2)
        if v == 255:
            return self.packNibble(n2)
        return -1

    def packHex(self, n):
        if n in range(48, 58):
            return n - 48
        if n in range(65, 71):
            return 10 + (n - 65)
        return -1

    def packNibble(self, n):
        if n in (45, 46):
            return 10 + (n - 45)

        if n in range(48, 58):
            return n - 48

        return -1
