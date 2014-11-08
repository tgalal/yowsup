from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ChallengeProtocolEntity(ProtocolEntity):
    def __init__(self, nonce):
        super(ChallengeProtocolEntity, self).__init__("challenge")
        self.nonce = nonce
    
    def getNonce(self):
        return self.nonce

    def toProtocolTreeNode(self):
        return self._createProtocolTreeNode({}, children = None, data = self.nonce)

    @staticmethod
    def fromProtocolTreeNode(node):

        nonce = list(map(ord,node.getData()))
        #entity = ChallengeProtocolEntity(bytearray(node.getData().decode("latin-1"), "latin-1"))
        entity = ChallengeProtocolEntity(bytearray(nonce))
        return entity
        # try:
        #     entity = ChallengeProtocolEntity(bytearray(node.getData().decode("latin-1"), "latin-1"))
        # except TypeError

        #return ChallengeProtocolEntity(node.getData())