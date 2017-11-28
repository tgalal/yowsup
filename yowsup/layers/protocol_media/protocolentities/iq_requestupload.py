from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
import hashlib
import base64
import os
from yowsup.common.tools import WATools
class RequestUploadIqProtocolEntity(IqProtocolEntity):
    '''
    <iq to="s.whatsapp.net" type="set" xmlns="w:m">
        <media hash="{{b64_hash}}" type="{{type}}" size="{{size_bytes}}" orighash={{b64_orighash?}}></media>
    </iq>
    '''

    MEDIA_TYPE_IMAGE = "image"
    MEDIA_TYPE_VIDEO = "video"
    MEDIA_TYPE_AUDIO = "audio"
    MEDIA_TYPE_DOCUMENT = "document"
    XMLNS = "w:m"

    TYPES_MEDIA = (MEDIA_TYPE_AUDIO, MEDIA_TYPE_IMAGE, MEDIA_TYPE_VIDEO, MEDIA_TYPE_DOCUMENT)

    def __init__(self, mediaType, b64Hash = None, size = None, origHash = None, filePath = None ):
        super(RequestUploadIqProtocolEntity, self).__init__("w:m", _type = "set", to = YowConstants.WHATSAPP_SERVER)

        assert (b64Hash and size) or filePath, "Either specify hash and size, or specify filepath and let me generate the rest"

        if filePath:
            assert os.path.exists(filePath), "Either specified path does not exist, or yowsup doesn't have permission to read: %s" % filePath
            b64Hash = self.__class__.getFileHashForUpload(filePath)

            size = os.path.getsize(filePath)


        self.setRequestArguments(mediaType, b64Hash, size, origHash)

    def setRequestArguments(self, mediaType, b64Hash, size, origHash = None):
        assert mediaType in self.__class__.TYPES_MEDIA, "Expected media type to be in %s, got %s" % (self.__class__.TYPES_MEDIA, mediaType)
        self.mediaType = mediaType
        self.b64Hash = b64Hash
        self.size = int(size)
        self.origHash = origHash

    @staticmethod
    def getFileHashForUpload(filePath):
        return WATools.getFileHashForUpload(filePath)

    def __str__(self):
        out = super(RequestUploadIqProtocolEntity, self).__str__()
        out += "Media Type: %s\n" % self.mediaType
        out += "B64Hash: %s\n" % self.b64Hash
        out += "Size: %s\n" % self.size
        if self.origHash:
            out += "OrigHash: %s\n" % self.origHash
        return out

    def toProtocolTreeNode(self):
        node = super(RequestUploadIqProtocolEntity, self).toProtocolTreeNode()
        attribs = {
            "hash": self.b64Hash,
            "type": self.mediaType,
            "size": str(self.size)
        }
        if self.origHash:
            attribs["orighash"] = self.origHash
        mediaNode = ProtocolTreeNode("encr_media", attribs)
        node.addChild(mediaNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        assert node.getAttributeValue("type") == "set", "Expected set as iq type in request upload, got %s" % node.getAttributeValue("type")
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RequestUploadIqProtocolEntity
        mediaNode = node.getChild("encr_media")
        entity.setRequestArguments(
            mediaNode.getAttributeValue("type"),
            mediaNode.getAttributeValue("hash"),
            mediaNode.getAttributeValue("size"),
            mediaNode.getAttributeValue("orighash")
        )
        return entity
