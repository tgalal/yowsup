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

        return protocolTreeNode.__class__ == ProtocolTreeNode\
            and self.tag == protocolTreeNode.tag\
            and self.data == protocolTreeNode.data\
            and set(self.children) == set(protocolTreeNode.children)\
            and self.attributes == protocolTreeNode.attributes

    def __hash__(self):
        return hash(self.tag) ^ hash(tuple(self.attributes.items())) ^ hash(self.data)

    def toString(self):
        out = "<"+self.tag;
        if self.attributes is not None:
            for key,val in self.attributes.items():
                out+= " "+key+'="'+val+'"'
        out+= ">\n";

        if self.data is not None:
            if type(self.data) is bytearray:
                out += self.data.decode()
            else:
                out += self.data;
        
        for c in self.children:
           out += c.toString()
        #print sel
        out+= "</"+self.tag+">\n"
        return out

    
    def __str__(self):
        return self.toString() 

    def getData(self):
        return self.data
        
    
    @staticmethod   
    def tagEquals(node,string):
        return node is not None and node.tag is not None and node.tag == string;
        
        
    @staticmethod
    def require(node,string):
        if not ProtocolTreeNode.tagEquals(node,string):
            raise Exception("failed require. string: "+string);
    

    def __getitem__(self, key):
        return self.getAttributeValue(key)

    def __setitem__(self, key, val):
        self.setAttribute(key, val)

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
