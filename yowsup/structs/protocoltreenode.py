import binascii


class ProtocolTreeNode(object):
    _STR_MAX_LEN_DATA = 500
    _STR_INDENT = '  '

    def __init__(self, tag, attributes = None, children = None, data = None):
        # type: (str, dict, list[ProtocolTreeNode], bytes) -> None
        if data is not None:
            assert type(data) is bytes, type(data)

        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.data = data
        self._truncate_str_data = True

        assert type(self.children) is list, "Children must be a list, got %s" % type(self.children)

    def __eq__(self, protocolTreeNode):
        """
        :param protocolTreeNode: ProtocolTreeNode
        :return: bool
        """
        #
        if protocolTreeNode.__class__ == ProtocolTreeNode\
            and self.tag == protocolTreeNode.tag\
            and self.data == protocolTreeNode.data\
            and self.attributes == protocolTreeNode.attributes\
            and len(self.getAllChildren()) == len(protocolTreeNode.getAllChildren()):
                found = False
                for c in self.getAllChildren():
                    for c2 in protocolTreeNode.getAllChildren():
                        if c == c2:
                            found = True
                            break
                    if not found:
                        return False

                found = False
                for c in protocolTreeNode.getAllChildren():
                    for c2 in self.getAllChildren():
                        if c == c2:
                            found = True
                            break
                    if not found:
                        return False

                return True

        return False

    def __hash__(self):
        return hash(self.tag) ^ hash(tuple(self.attributes.items())) ^ hash(self.data)

    def __str__(self):
        out = "<%s" % self.tag
        attrs = " ".join((map(lambda item: "%s=\"%s\"" % item, self.attributes.items())))
        children = "\n".join(map(str, self.children))
        data = self.data or b""
        len_data = len(data)

        if attrs:
            out = "%s %s" % (out, attrs)

        if children or data:
            out = "%s>" % out
            if children:
                out = "%s\n%s%s" % (out, self._STR_INDENT, children.replace('\n', '\n' + self._STR_INDENT))
            if len_data:
                if self._truncate_str_data and len_data > self._STR_MAX_LEN_DATA:
                    data = data[:self._STR_MAX_LEN_DATA]
                    postfix = "...[truncated %s bytes]" % (len_data - self._STR_MAX_LEN_DATA)
                else:
                    postfix = ""
                data = "0x%s" % binascii.hexlify(data).decode()
                out = "%s\n%s%s%s" % (out, self._STR_INDENT, data, postfix)

            out = "%s\n</%s>" % (out, self.tag)
        else:
            out = "%s />" % out

        return out

    def getData(self):
        return self.data

    def setData(self, data):
        self.data = data


    @staticmethod
    def tagEquals(node,string):
        return node is not None and node.tag is not None and node.tag == string


    @staticmethod
    def require(node,string):
        if not ProtocolTreeNode.tagEquals(node,string):
            raise Exception("failed require. string: "+string);


    def __getitem__(self, key):
        return self.getAttributeValue(key)

    def __setitem__(self, key, val):
        self.setAttribute(key, val)

    def __delitem__(self, key):
        self.removeAttribute(key)


    def getChild(self,identifier):

        if type(identifier) == int:
            if len(self.children) > identifier:
                return self.children[identifier]
            else:
                return None

        for c in self.children:
            if identifier == c.tag:
                return c

        return None

    def hasChildren(self):
        return len(self.children) > 0

    def addChild(self, childNode):
        self.children.append(childNode)

    def addChildren(self, children):
        for c in children:
            self.addChild(c)

    def getAttributeValue(self,string):
        try:
            return self.attributes[string]
        except KeyError:
            return None

    def removeAttribute(self, key):
        if key in self.attributes:
            del self.attributes[key]

    def setAttribute(self, key, value):
        self.attributes[key] = value

    def getAllChildren(self,tag = None):
        ret = []
        if tag is None:
            return self.children

        for c in self.children:
            if tag == c.tag:
                ret.append(c)

        return ret
