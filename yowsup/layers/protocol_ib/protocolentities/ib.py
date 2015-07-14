from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class IbProtocolEntity(ProtocolEntity):
    '''
    <ib></ib>
    '''
    def __init__(self):
        super(IbProtocolEntity, self).__init__("ib")
    
    def toProtocolTreeNode(self):
        return self._createProtocolTreeNode({}, None, None)

    def __str__(self):
        out  = "Ib:\n"
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return IbProtocolEntity()
