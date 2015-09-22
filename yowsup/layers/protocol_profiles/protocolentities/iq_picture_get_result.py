from .iq_picture import PictureIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class ResultGetPictureIqProtocolEntity(PictureIqProtocolEntity):
    '''
    <iq type="result" from="{{jid}}" id="{{id}}">
        <picture type="image | preview" id="{{another_id}}">
        {{Binary bytes of the picture.}}
        </picture>
    </iq>
    '''
    def __init__(self, jid, pictureData, pictureId, preview = True, _id = None):
        super(ResultGetPictureIqProtocolEntity, self).__init__(jid, _id, "result")
        self.setResultPictureProps(pictureData, pictureId, preview)

    def setResultPictureProps(self, pictureData, pictureId, preview = True):
        self.preview = preview
        self.pictureData = pictureData
        self.pictureId = pictureId

    def isPreview(self):
        return self.preview

    def getPictureData(self):
        return self.pictureData

    def getPictureId(self):
        return self.pictureId

    def writeToFile(self, path):
        with open(path, "wb") as outFile:
            outFile.write(self.getPictureData())

    def toProtocolTreeNode(self):
        node = super(ResultGetPictureIqProtocolEntity, self).toProtocolTreeNode()
        pictureNode = ProtocolTreeNode({"type": "preview" if self.isPreview() else "image" }, data = self.getPictureData())
        node.addChild(pictureNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PictureIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ResultGetPictureIqProtocolEntity
        pictureNode = node.getChild("picture")
        entity.setResultPictureProps(pictureNode.getData(), pictureNode.getAttributeValue("id"), pictureNode.getAttributeValue("type") == "preview")
        return entity