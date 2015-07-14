from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class StreamFeaturesProtocolEntity(ProtocolEntity):
    def __init__(self,  features = None):
        super(StreamFeaturesProtocolEntity, self).__init__("stream:features")
        self.setFeatures(features)

    def setFeatures(self, features = None):
        self.features = features or []

    def toProtocolTreeNode(self):
        featureNodes = [ProtocolTreeNode(feature) for feature in self.features]
        return self._createProtocolTreeNode({}, children = featureNodes, data = None)


    @staticmethod
    def fromProtocolTreeNode(node):
        return StreamFeaturesProtocolEntity([fnode.tag for fnode in node.getAllChildren()])