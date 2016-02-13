import binascii
import sys
class ProtocolTreeNode(object):
    def __init__(self, tag, attributes = None, children = None, data = None):

        self.tag = tag
        self.attributes = attributes or {}
        self.children = children or []
        self.data = data

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

    def toString(self):
        out = "<"+self.tag
        if self.attributes is not None:
            for key,val in self.attributes.items():
                if val is None:
                    raise ValueError("value is none for attr %s" % key)
                out+= " "+key+'="'+val+'"'
        out+= ">\n"

        if self.data is not None:
            if type(self.data) is bytearray:
                try:
                    out += "%s" % self.data.decode()
                except UnicodeDecodeError:
                    out += binascii.hexlify(self.data)
            else:
                try:
                    out += "%s" % self.data
                except UnicodeDecodeError:
                    try:
                        out += "%s" % self.data.decode()
                    except UnicodeDecodeError:
                        out += binascii.hexlify(self.data)

            if type(self.data) is str and sys.version_info >= (3,0):
                out += "\nHEX3:%s\n" % binascii.hexlify(self.data.encode('latin-1'))
            else:
                out += "\nHEX:%s\n" % binascii.hexlify(self.data)

        for c in self.children:
            try:
                out += c.toString()
            except UnicodeDecodeError:
                out += "[ENCODED DATA]\n"
        out+= "</"+self.tag+">\n"
        return out


    def __str__(self):
        return self.toString()

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
