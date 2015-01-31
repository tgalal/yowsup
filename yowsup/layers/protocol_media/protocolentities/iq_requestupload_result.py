from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class ResultRequestUploadIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_requestupload_result.xsd")
    def __init__(self, _id, url, ip = None, resumeOffset = 0, duplicate = False, filehash = None, mimeType = None, size = None, width = None, height = None):
        super(ResultRequestUploadIqProtocolEntity, self).__init__(_id = _id, _from = "s.whatsapp.net", _type="result")
        self.setUploadProps(url, ip, resumeOffset, duplicate, filehash, mimeType, size, width, height)

    def setUploadProps(self, url ,ip, resumeOffset, duplicate, filehash, mimeType, size, width, height):
        self.url = url
        self.ip = ip
        self.resumeOffset = resumeOffset or 0
        self.duplicate = duplicate
        self.filehash = filehash
        self.mimeType = mimeType
        self.width = int(width) if width else None
        self.height = int(height) if height else None
        self.size = int(size) if size else None

    def isDuplicate(self):
        return self.duplicate

    def getUrl(self):
        return self.url

    def getResumeOffset(self):
        return self.resumeOffset

    def getIp(self):
        return self.ip

    def __str__(self):
        out = super(ResultRequestUploadIqProtocolEntity, self).__str__()
        out += "URL: %s\n" % self.url
        if self.ip:
            out += "IP: %s\n" % self.ip
        return out

    def toProtocolTreeNode(self):
        node = super(ResultRequestUploadIqProtocolEntity, self).getProtocolTreeNode()

        if not self.isDuplicate():
            mediaNode = ProtocolTreeNode("media", {"url": self.url}, parent=node)
            if self.ip:
                mediaNode["ip"] = self.ip

            if self.resumeOffset:
                mediaNode["resume"] = str(self.resumeOffset)
        else:
            dupNode = ProtocolTreeNode("duplicate", {"url": self.url}, parent=node)
            if self.mimeType:
                dupNode["mimetype"] = self.mimeType
                dupNode["type"] = self.mimeType.split('/')[0]

            if self.width:
                dupNode["width"] = str(self.width)

            if self.height:
                dupNode["height"] = str(self.height)

            if self.filehash:
                dupNode["filehash"] = self.filehash

            if self.size:
                dupNode["size"] = str(self.size)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        childNode = node.getChild("media")
        duplicate = False
        if childNode is None:
            childNode = node.getChild("duplicate")
            duplicate = True


        entity = ResultRequestUploadIqProtocolEntity(node["id"],
                                                     childNode["url"], childNode["ip"],
                                                     childNode["resume"], duplicate,
                                                     childNode["filehash"], childNode["mimetype"],
                                                     childNode["size"], childNode["width"], childNode["height"]
        )

        return entity
