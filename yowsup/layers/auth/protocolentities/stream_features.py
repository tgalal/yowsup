from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class StreamFeaturesProtocolEntity(ProtocolEntity):
    def __init__(self, receipt_acks = False):
        super(StreamFeaturesProtocolEntity, self).__init__("stream:features")
        self.receiptAcks = receipt_acks
    
    def toProtocolTreeNode(self):
        features = []
        if self.supportsReceiptAcks():
            features.append(ProtocolTreeNode("receipt_acks", {}))
        return self._createProtocolTreeNode({}, children = features, data = None)


    def supportsReceiptAcks(self):
        return self.receiptAcks

    @staticmethod
    def fromProtocolTreeNode(node):
        return StreamFeaturesProtocolEntity(node.getChild("receipt_acks") is not None)