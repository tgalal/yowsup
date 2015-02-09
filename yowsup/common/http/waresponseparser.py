import json, sys
from xml.dom import minidom
import plistlib
import logging
logger = logging.getLogger(__name__)

class ResponseParser(object):
    def __init__(self):
        self.meta = "*"
        
    def parse(self, text, pvars):
        return text
    
    def getMeta(self):
        return self.meta
    
    
    def getVars(self, pvars):

        if type(pvars) is dict:
            return pvars

        if type(pvars) is list:
            
            out = {}
            
            for p in pvars:
                out[p] = p
                
            return out

class XMLResponseParser(ResponseParser):
    
    def __init__(self):
        
        try:
            import libxml2
        except ImportError:
            print("libxml2 XMLResponseParser requires libxml2")
            sys.exit(1)

        self.meta = "text/xml";

    def parse(self, xml, pvars):
        import libxml2
        doc = libxml2.parseDoc(xml)
        
        pvars = self.getVars(pvars)
        vals = {}
        for k, v in pvars.items():
            res = doc.xpathEval(v)
            vals[k] = []
            for r in res:
                
                #if not vals.has_key(r.name):
                #   vals[r.name] = []
                
                if r.type == 'element':
                    #vals[r.name].append(self.xmlToDict(minidom.parseString(str(r)))[r.name])
                    vals[k].append(self.xmlToDict(minidom.parseString(str(r)))[r.name])
                elif r.type == 'attribute':
                    vals[k].append(r.content)
                else:
                    logger.error("UNKNOWN TYPE")
            
            if len(vals[k]) == 1:
                vals[k] = vals[k][0]
            elif len(vals[k]) == 0:
                vals[k] = None

        return vals
    
    def xmlToDict(self, xmlNode):
        if xmlNode.nodeName == "#document":
            
            node = {xmlNode.firstChild.nodeName:{}}
            
            node[xmlNode.firstChild.nodeName] = self.xmlToDict(xmlNode.firstChild)
            return node
        
        node = {}
        curr = node
        
        if xmlNode.attributes:
            for name, value in xmlNode.attributes.items():
                curr[name] = value

        for n in xmlNode.childNodes:
            
            if n.nodeType == n.TEXT_NODE:
                curr["__TEXT__"] = n.data
                continue
            
            if not n.nodeName in curr:
                curr[n.nodeName] = []

            if len(xmlNode.getElementsByTagName(n.nodeName)) > 1:
                #curr[n.nodeName] = []
                curr[n.nodeName].append(self.xmlToDict(n))
            else:
                curr[n.nodeName] = self.xmlToDict(n)
            
            
        return node

class JSONResponseParser(ResponseParser):
    
    def __init__(self):
        self.meta = "text/json"

    def parse(self, jsonData, pvars):
        
        d = json.loads(jsonData)
        pvars = self.getVars(pvars)
        
        parsed = {}     
        
        for k,v in pvars.items():
            parsed[k] = self.query(d, v)

        return parsed
    
    def query(self, d, key):
        keys = key.split('.', 1)
            
        currKey = keys[0]
        
        if(currKey in d):
            item = d[currKey]
            
            if len(keys) == 1:
                    return item
            
            if type(item) is dict:
                return self.query(item, keys[1])
            
            elif type(item) is list:
                output = []

                for i in item:
                    output.append(self.query(i, keys[1]))
                return output
            
            else:
                return None

class PListResponseParser(ResponseParser):
    def __init__(self):
        self.meta = "text/xml"
    
    def parse(self, xml, pvars):
        
        #tmp = minidom.parseString(xml)
        
        if sys.version_info >= (3, 0):
            pl = plistlib.readPlistFromBytes(xml.encode());
        else:
            pl = plistlib.readPlistFromString(xml);
        
        parsed= {}
        pvars = self.getVars(pvars)
        
        for k,v in pvars.items():
            parsed[k] = pl[k] if  k in pl else None
        
        return parsed;
        
