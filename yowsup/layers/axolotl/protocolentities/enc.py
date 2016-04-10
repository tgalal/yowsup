from yowsup.structs import ProtocolEntity, ProtocolTreeNode
import sys
class EncProtocolEntity(ProtocolEntity):
    TYPE_PKMSG  = "pkmsg"
    TYPE_MSG    = "msg"
    TYPE_SKMSG  = "skmsg"
    TYPES = (TYPE_PKMSG, TYPE_MSG, TYPE_SKMSG)

    def __init__(self, type, version, data, mediaType = None, jid = None):
        assert type in self.__class__.TYPES, "Unknown message enc type %s" % type
        super(EncProtocolEntity, self).__init__("enc")
        self.type = type
        self.version = int(version)
        self.data = data
        self.mediaType = mediaType
        self.jid = jid

    def getType(self):
        return self.type

    def getVersion(self):
        return self.version

    def getData(self):
        return self.data

    def getMediaType(self):
        return self.mediaType

    def getJid(self):
        return self.jid

    def toProtocolTreeNode(self):
        attribs = {"type": self.type, "v": str(self.version)}
        if self.mediaType:
            attribs["mediatype"] = self.mediaType
        encNode =  ProtocolTreeNode("enc", attribs, data = self.data)
        if self.jid:
            return ProtocolTreeNode("to", {"jid": self.jid}, [encNode])
        return encNode

    @staticmethod
    def fromProtocolTreeNode(node):
        return EncProtocolEntity(node["type"], node["v"], node.data.encode('latin-1') if sys.version_info >= (3,0) else node.data, node["mediatype"])
