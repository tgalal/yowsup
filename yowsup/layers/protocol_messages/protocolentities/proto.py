from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ProtoProtocolEntity(ProtocolEntity):

    def __init__(self, protoData, mediaType = None):
        super(ProtoProtocolEntity, self).__init__("proto")
        self.mediaType = mediaType
        self.protoData = protoData

    def getProtoData(self):
        return self.protoData

    def getMediaType(self):
        return self.mediaType

    def toProtocolTreeNode(self):
        attribs = {}
        if self.mediaType:
            attribs["mediatype"] = self.mediaType
        return ProtocolTreeNode("proto", attribs, data=self.protoData)

    @staticmethod
    def fromProtocolTreeNode(node):
        return ProtoProtocolEntity(node.data, node["mediatype"])