from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ChallengeProtocolEntity(ProtocolEntity):
    def __init__(self, nonce):
        super(ChallengeProtocolEntity, self).__init__("challenge")
        self.nonce = nonce
    
    def getNonce(self):
        return self.nonce

    def toProtocolTreeNode(self):
        #return self._createProtocolTreeNode({}, children = None, data = self.nonce)
        return self._createProtocolTreeNode({}, children = [], data = "".join(map(chr, self.nonce)))

    def __str__(self):
        out = "Challenge\n"
        out += "Nonce: %s\n" % self.nonce
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        nonce = list(map(ord,node.getData()))
        entity = ChallengeProtocolEntity(bytearray(nonce))
        return entity
