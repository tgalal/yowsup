from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class PictureIqProtocolEntity(IqProtocolEntity):
    '''
    When asking for a profile picture:
    <iq type="get" id="{{id}}" xmlns="w:profile:picture", to={{jid}}">
        <picture type="image | preview">
        </picture>
    </iq>

    When receiving a profile picture:
    <iq type="result" from="{{jid}}" id="{{id}}">
        <picture type="image" id="{{another_id}}">
        {{Binary bytes of the picture.}}
        </picture>
    </iq>

    FIXME: not tested yet, does it work?:
    When setting a profile picture:
    <iq type="set" id="{{id}}" xmlns="w:profile:picture", to={{jid}}">
        <picture type="image">
        {{Binary bytes of the picture when type is set.}}
        </picture>
    </iq>
    '''

    def __init__(self, jid, type="get", largeFormat = True):
        super(PictureIqProtocolEntity, self).__init__("w:profile:picture", _type=type, to=jid, _id=("set_photo_" + self._generateId(True) if type=="set" else None))
        self.pictureId = None
        self.pictureData = None
        self.previewData = None
        self.largeFormat = largeFormat

    def __str__(self):
        out  = super(PictureIqProtocolEntity, self).__str__()
        if self.pictureData is not None:
            out += "pictureData: Binary data\n"
        if self.pictureId is not None:
            out += "pictureId: %s\n" % self.pictureId
        return out

    def setPictureData(self, pictureData):
        self.pictureData = pictureData

    def setPreviewData(self, previewData):
        self.previewData = previewData

    def getPictureData(self):
        return self.pictureData

    def getPreviewData(self):
        return self.previewData

    def setPictureId(self, pictureId):
        self.pictureId = pictureId

    def getPictureId(self):
        return self.pictureId

    def toProtocolTreeNode(self):
        node = super(PictureIqProtocolEntity, self).toProtocolTreeNode()
        # if self._type == "set" and self.pictureId is None:
        #     self.pictureId = self._generateId(True)
        if self._type == "get":
            if self.pictureId is None:
                attribs = {"type": "image" if self.largeFormat else "preview"}
            else:
                attribs = {"type": "image" if self.largeFormat else "preview", "id": self.pictureId}
            pictureNode = ProtocolTreeNode("picture", attribs, None, self.pictureData)
            node.addChild(pictureNode)
        else:
            if self.pictureId is None:
                attribs = {"type": "image"}
            else:
                attribs = {"type": "image", "id": self.pictureId}
            pictureNode = ProtocolTreeNode("picture", attribs, None, self.pictureData)
            node.addChild(pictureNode)

            if self.previewData is not None or not self.largeFormat:
                if self.pictureId is None:
                    attribs = {"type": "preview"}
                else:
                    attribs = {"type": "preview", "id": self.pictureId}
                pictureNode = ProtocolTreeNode("picture", attribs, None, self.previewData)
                node.addChild(pictureNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = PictureIqProtocolEntity
        entity.pictureId = None
        entity.pictureData = None
        entity.previewData = None
        entity.largeFormat = False
        pictureNode = node.getChild("picture")
        # assert pictureNode["type"] == "image", "Not a profile picture with type image, got %s" \
        #     % pictureNode["type"]
        if pictureNode["type"] == "image":
            entity.setPictureData(pictureNode.getData())
            entity.largeFormat = True
        elif pictureNode["type"] == "preview":
            entity.setPreviewData(pictureNode.getData())
            entity.largeFormat = False
        entity.setPictureId(pictureNode["id"])
        return entity

