from lxml import etree
import binascii
import sys

def ProtocolTreeNode(tag = None, attributes = None, children = None , data = None, ns = None, dataEncoding = None, xmlString = None):
    assert bool(tag) ^ bool(xmlString), "Must provide either tag or xmlString"
    assert bool(xmlString) ^ (bool(tag) or bool(attributes) or bool(children) or bool(data) or bool(data) or bool(dataEncoding)), "Either XML string or xml data"

    if tag and ":" in tag:
        tagNS, tagName = tag.split(':')
        tag = "{%s}%s" % (tagNS, tagName)
        if not ns:
            ns = (tagNS, tagNS)

    return _ProtocolTreeNode.new(tag, attributes, children, data, ns, dataEncoding) if tag else _ProtocolTreeNode.fromXML(xmlString)

class _ProtocolTreeNode(etree.ElementBase):
    parser = None

    hexlify = ("response", "success", "challenge", "registration", "identity", "value", "id", "signature", "enc", "type")

    @staticmethod
    def new(tag, attributes = None, children = None , data = None, ns = None, dataEncoding = None):
        _ProtocolTreeNode.__ensureParser()
        attributes = attributes or {}
        children = children or []
        if dataEncoding is None and tag in _ProtocolTreeNode.hexlify:
            dataEncoding = "hex"
        nsmap = {}

        if ns is not None:
            nsmap[ns[0]] = ns[1]

        element = _ProtocolTreeNode.parser.makeelement(tag, nsmap = nsmap)
        element.setData(data, dataEncoding)
        element.addChildren(children)
        for k, v in attributes.items():
            element.setAttribute(k, v)

        return element

    def getTag(self):
        tag = self.tag
        nsmap = self.nsmap
        if None in self.nsmap:
            tag = tag.replace("{%s}" % nsmap[None], "")

        return tag

    @staticmethod
    def __ensureParser():
        if _ProtocolTreeNode.parser is None:
            _ProtocolTreeNode.parser = etree.XMLParser()
            _ProtocolTreeNode.parser.set_element_class_lookup(
                 etree.ElementDefaultClassLookup(element = _ProtocolTreeNode)
            )

    @staticmethod
    def fromXML(xml):
        _ProtocolTreeNode.__ensureParser()
        return etree.fromstring(xml, _ProtocolTreeNode.parser)


    def __getitem__(self, key):
        if type(key) is str:
            return self.getAttributeValue(key)
        return super(_ProtocolTreeNode, self).__getitem__(key)

    def __setitem__(self, key, val):
        if type(key) is str:
            return self.setAttribute(key, val)
        return super(_ProtocolTreeNode, self).__setitem__(key, val)


    def __delitem__(self, key):
        if type(key) is str:
            return self.removeAttribute(key)
        return super(_ProtocolTreeNode, self).__delitem__(key)


    def __eq__(self, protocolTreeNode):
        """
        :param protocolTreeNode: ProtocolTreeNode
        :return: bool
        """
        #


        #
        # for debugging:
        #
        # if protocolTreeNode.getTag() == "iq" and protocolTreeNode["id"] == "111111":
        #     me = self#.getChild(0)
        #     them = protocolTreeNode#.getChild(0)
        #
        #     print(me.getAttributes())
        #     print(them.getAttributes())
        #
        #     if them.__class__ == _ProtocolTreeNode \
        #         and me.getTag() == them.getTag() \
        #         and me.getData()  == them.getData() \
        #         and me.getAttributes() == them.getAttributes():
        #         # and len(me.getAllChildren()) == len(them.getAllChildren()):
        #         print("OKKKKK")


        if protocolTreeNode.__class__ == _ProtocolTreeNode \
                and self.getTag() == protocolTreeNode.getTag() \
                and self.getData()  == protocolTreeNode.getData() \
                and self.getAttributes() == protocolTreeNode.getAttributes() \
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
        return hash(self.tag) ^ hash(tuple(self.getAttributes().items())) ^ hash(self.getData())

    def getAttributes(self, includeNamepsace = False):
        result = {}
        for k in self.attrib:
            if k.startswith("meta-yowsup"):
                continue
            if k == "xmlns" and not includeNamepsace:
                continue
            result[k] = self.getAttributeValue(k)

        if includeNamepsace and None in self.nsmap:
            result["xmlns"] = self.nsmap[None]
        return result

    def getLocalName(self):
        tag = self.getTag()
        return tag.split(':')[1] if ':' in tag else tag

    def toPrettyXml(self):
        return etree.tostring(self, pretty_print = True)

    def __str__(self, ensureNamespace = True):
        # if ensureNamespace and ":" in self.getTag():
        #     ns = self.getTag().split(':')[0]
        #     attrib = "xmlns:%s" % ns
        #     if not self.hasAttribute(attrib):
        #         self.setAttribute(attrib, ns)
        #         result = self.toPrettyXml()
        #         self.removeAttribute(attrib)
        #         return result

        result = self.toPrettyXml()
        if type(result == bytes):
            result = result.decode('utf-8')

        return result


    def getData(self):
        if self.text:
            encoding = self.getMetaAttribute("encoding", "unicode_escape")
            if encoding == "hex":
                data = binascii.unhexlify(self.text.encode()).decode("latin-1")
            else:
                data = self.text.encode().decode(encoding)
            if sys.version_info < (3,0) and type(data) is unicode:
                data = data.encode("latin-1")

            if not data.strip():
                return None

            return data

    def setData(self, data, dataEncoding = None):
        if data is not None:
            if type(data) is bytes:
                data = data.decode('latin-1')

            if dataEncoding:
                self.setMetaAttribute("encoding", dataEncoding)
            else:
                dataEncoding = "unicode_escape"

            if dataEncoding == "hex":
                self.text = binascii.hexlify(data.encode("latin-1"))
            else:
                self.text = data.encode(dataEncoding)

    def setMetaAttribute(self, key, val):
        self.setAttribute("meta-yowsup-" + key, val)

    def getMetaAttribute(self, key, default = None):
        return self.getAttributeValue("meta-yowsup-" + key) or default

    def _getData(self):
        if self.text:
            hexEncoded = self.text.startswith("0x")
            if not hexEncoded:
                return self.text

            data = binascii.unhexlify(self.text[2:])
            return data #if sys.version_info < (3, 0) else data.decode()

    def _setData(self, data):
        if data:
            try:
                self.text = data
            except ValueError:
                if type(data) is not bytes:
                    data = data.encode()

                self.text = binascii.hexlify(data)
                self.text = "0x" + self.text

                # if sys.version_info < (3,0):
                #     self.text =  "0x" + binascii.hexlify(data)
                # else:
                #     self.text =  binascii.hexlify(data)


    @staticmethod
    def tagEquals(node,string):
        return node is not None and node.tag is not None and node.tag == string


    @staticmethod
    def require(node,string):
        if not _ProtocolTreeNode.tagEquals(node,string):
            raise Exception("failed require. string: "+string)

    def hasAttribute(self, attr):
        return attr in self.attrib

    def getChild(self,identifier):

        if type(identifier) == int:
            if len(self.getAllChildren()) > identifier:
                return self.getAllChildren()[identifier]
            else:
                return None
        for c in self.getAllChildren():
            if c.getTag(

            ) == identifier:
                return c


    def hasChildren(self):
        return len(self.getAllChildren()) > 0

    def addChild(self, childNode):
        self.append(childNode)

    def addChildren(self, children):
        for c in children:
            self.addChild(c)

    def getAttributeValue(self,string):
        val = self.get(string)
        return val if val != '' else None

    def removeAttribute(self, key):
        if key in self.attrib:
            del self.attrib[key]

    def setAttribute(self, key, value):
        if type(value) is int:
            value = str(value)
        self.set(key ,value)

    def getAllChildren(self,tag = None):
        return self.findall(tag) if tag is not None else self[:]
