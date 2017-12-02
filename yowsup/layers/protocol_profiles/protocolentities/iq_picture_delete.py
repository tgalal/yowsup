from .iq_picture import PictureIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
import time
class DeletePictureIqProtocolEntity(PictureIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:profile:picture", to={{jid}}">
        <picture type="image" id="{{another_id}}">
        {{Binary bytes of the picture when type is set.}}
        </picture>
    </iq>
'''
    def __init__(self, jid, _id = None):
        super(DeletePictureIqProtocolEntity, self).__init__(jid, _id, "delete")


    def toProtocolTreeNode(self):
        node = super(PictureIqProtocolEntity, self).toProtocolTreeNode()
        #attribs = {"type": "image", "id": self.pictureId}
        #pictureNode = ProtocolTreeNode("picture", attribs, None, None)
        #node.addChild(pictureNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PictureIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DeletePictureIqProtocolEntity

        pictureNode = None
        previewNode = None

        for child in node.getAllChildren("picture"):
            nodeType = child.getAttributeValue("type")
            if nodeType == "image":
                pictureNode = child
            elif nodeType == "preview":
                previewNode = child
        if pictureNode and previewNode:
            entity.setSetPictureProps(previewNode.getData(), pictureNode.getData(), pictureNode.getAttributeValue("id"))
        return entity
