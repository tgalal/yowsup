from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class DecProtocolEntity(ProtocolEntity):
    TYPE_MEDIA_IMAGE="image"
    TYPE_MEDIA_VIDEO="video"
    TYPE_MEDIA_AUDIO="audio"
    TYPE_MEDIA_CONTACT="contact"
    TYPE_MEDIA_LOCATION="location"
    TYPE_MEDIA_DOCUMENT="document"
    TYPES_MEDIA = (None, TYPE_MEDIA_IMAGE, TYPE_MEDIA_AUDIO, TYPE_MEDIA_VIDEO, TYPE_MEDIA_CONTACT, TYPE_MEDIA_LOCATION,
                   TYPE_MEDIA_DOCUMENT)

    def __init__(self, data, mediaType = None):
        assert mediaType in self.__class__.TYPES_MEDIA, "Unknown message media type %s" % type
        super(DecProtocolEntity, self).__init__("dec")
        self.mediaType = mediaType
        self.data = data

    def getData(self):
        return self.data

    def getMediaType(self):
        return self.mediaType

    def toProtocolTreeNode(self):
        attribs = {}
        if self.mediaType:
            attribs["mediatype"] = self.mediaType
        return ProtocolTreeNode("dec", attribs, data=self.data)

    @staticmethod
    def fromProtocolTreeNode(node):
        return DecProtocolEntity(node.data, node["mediatype"])
