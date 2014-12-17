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
        data.append(5)

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

        x = 1 + (0 if node.attributes is None else len(node.attributes) * 2) + (0 if not node.hasChildren() else 1) + (0 if node.data is None else 1)

        self.writeListStart(1 + (0 if node.attributes is None else len(node.attributes) * 2) + (0 if not node.hasChildren() else 1) + (0 if node.data is None else 1), data)

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
                self.writeString(value, data);


    def writeBytes(self, bytes, data):

        length = len(bytes)
        if length >= 256:
            data.append(253)
            self.writeInt24(length, data)
        else:
            data.append(252)
            self.writeInt8(length, data)

        for b in bytes:
            if type(b) is int:
                data.append(b)
            else:
                data.append(ord(b))

    def writeInt8(self, v, data):
        data.append(v & 0xFF)


    def writeInt16(self, v, data):
        data.append((v & 0xFF00) >> 8);
        data.append((v & 0xFF) >> 0);


    def writeInt24(self, v, data):
        data.append((v & 0xFF0000) >> 16)
        data.append((v & 0xFF00) >> 8)
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

    def writeToken(self, intValue, data):
        if intValue < 245:
            data.append(intValue)
        elif intValue <=500:
            data.append(254)
            data.append(intValue - 245)

    def writeString(self, tag, data):
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
                self.writeBytes(self.encodeString(tag), data)

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
            self.writeString(user, data)
        else:
            self.writeToken(0, data)
        self.writeString(server, data)

