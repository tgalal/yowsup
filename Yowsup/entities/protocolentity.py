class ProtocolEntity:
    def __init__(self, tag):
        self.tag = tag

    def getTag(self):
        return self.tag
    
    def _createProtocolTreeNode(self, attributes, children = None, data = None):
        return ProtocolTreeNode(self.getTag(), attributes, children, data)
        
    
    def toProtocolTreeNode(self):
        pass

    def fromProtocolTreeNode(self, protocolTreeNode):
        pass
