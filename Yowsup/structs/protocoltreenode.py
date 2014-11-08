class ProtocolTreeNode():
    
    def __init__(self, tag, attributes, children = None, data = None):

        
        self.tag = tag;
        self.attributes = attributes;
        self.children = children;
        self.data = data
        
    def toString(self):
        try:
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
            
            if self.children is not None:
                for c in self.children:
                    out += c.toString();
            #print sel
            out+= "</"+self.tag+">\n"
            return out
        except TypeError:
            print("ignored toString call, probably encountered byte")
        except UnicodeDecodeError:
            print("ingnored toString call, encountered unicode error")

    
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
    
    
    def getChild(self,identifier):

        if self.children is None or len(self.children) == 0:
            return None
        if type(identifier) == int:
            if len(self.children) > identifier:
                return self.children[identifier]
            else:
                return None

        for c in self.children:
            if identifier == c.tag:
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

    def getAllChildren(self,tag = None):
        ret = [];
        if self.children is None:
            return ret;
            
        if tag is None:
            return self.children
        
        for c in self.children:
            if tag == c.tag:
                ret.append(c)
        
        return ret; 
