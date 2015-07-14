from .iq_picture import PictureIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class GetPictureIqProtocolEntity(PictureIqProtocolEntity):
    '''
    <iq type="get" id="{{id}}" xmlns="w:profile:picture", to={{jid}}">
        <picture type="image | preview">
        </picture>
    </iq>'''
    def __init__(self, jid, preview = True, _id = None):
        super(GetPictureIqProtocolEntity, self).__init__(jid, _id, "get")
        self.setGetPictureProps(preview)

    def setGetPictureProps(self, preview = True):
        self.preview = preview

    def isPreview(self):
        return self.preview

    def toProtocolTreeNode(self):
        node = super(GetPictureIqProtocolEntity, self).toProtocolTreeNode()
        pictureNode = ProtocolTreeNode("picture", {"type": "preview" if self.isPreview() else "image" })
        node.addChild(pictureNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PictureIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GetPictureIqProtocolEntity
        entity.setGetPictureProps(node.getChild("picture").getAttributeValue("type"))
        return entity