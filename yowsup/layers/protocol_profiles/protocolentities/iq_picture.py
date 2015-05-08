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
        <picture type="image" id="{{another_id}}">
        {{Binary bytes of the picture when type is set.}}
        </picture>
    </iq>
    '''
    XMLNS = "w:profile:picture"

    def __init__(self, jid, _id = None, type = "get"):
        super(PictureIqProtocolEntity, self).__init__(self.__class__.XMLNS, _id = _id, _type=type, to = jid)
        self.pictureData = None
        self.previewData = None
        self.pictureId = None

    def __str__(self):
        out  = super(PictureIqProtocolEntity, self).__str__()
        if self.pictureData is not None:
            out += "pictureData: Binary data\n"
        if self.previewData is not None:
            out += "previewData: Binary data\n"
        if self.pictureId is not None:
            out += "pictureId: %s\n" % self.pictureId
        return out

    def setPictureData(self, pictureData):
        self.pictureData = pictureData

    def getPictureData(self):
        return self.pictureData

    def setPreviewData(self, previewData):
        self.previewData = previewData
        
    def getPreviewData(self):
        return self.pictureData

    def setPictureId(self, pictureId):
        self.pictureId = pictureId

    def getPictureId(self):
        return self.pictureId

    def toProtocolTreeNode(self):
        node = super(PictureIqProtocolEntity, self).toProtocolTreeNode()
        if self._type == "set" and self.pictureId is None:
            self.pictureId = self._generateId(True)
        if self.pictureId is not None:
            attribs = {"type": "image", "id": self.pictureId}
        else:
            attribs = {"type": "image"}
        if self.pictureData is not None:
          pictureNode = ProtocolTreeNode("picture", attribs, None, self.pictureData)
          node.addChild(pictureNode)
        if self.previewData is not None:
          previewNode = ProtocolTreeNode("picture", {"type": "preview"}, None, self.previewData)
          node.addChild(previewNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = PictureIqProtocolEntity
        entity.__init__(entity.to, entity._id, entity._type)
        children = node.getAllChildren("picture")
        for child in children:
          nodeType = child.getAttributeValue("type")
          if nodeType == "image":
            entity.setPictureData(child.getData())
            entity.setPictureId(child["id"])
          elif nodeType == "preview":
            entity.setPreviewData(child.getData())
          else:
            entity.setPictureId(child["id"])
        return entity
