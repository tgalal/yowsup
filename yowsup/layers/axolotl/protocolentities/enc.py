from yowsup.structs import ProtocolEntity, ProtocolTreeNode

class EncProtocolEntity(ProtocolEntity):
    TYPE_PKMSG  = "pkmsg"
    TYPE_MSG    = "msg"
    TYPE_SKMSG  = "skmsg"
    TYPES = (TYPE_PKMSG, TYPE_MSG, TYPE_SKMSG)
    def __init__(self, type, version, data):
        assert type in self.__class__.TYPES, "Unknown message enc type %s" % type
        super(EncProtocolEntity, self).__init__("enc")
        self.type = type
        self.version = int(version)
        self.data = data

    def getType(self):
        return self.type

    def getVersion(self):
        return self.version

    def getData(self):
        return self.data

    def toProtocolTreeNode(self):
        return ProtocolTreeNode("enc", {"type": self.type, "v": str(self.version)}, data = self.data)

    @staticmethod
    def fromProtocolTreeNode(node):
        return EncProtocolEntity(node["type"], node["v"], node.data)
