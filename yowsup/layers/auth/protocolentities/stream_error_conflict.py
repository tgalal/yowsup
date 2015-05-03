from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class StreamErrorConflictProtocolEntity(ProtocolEntity):
    '''
     <stream:error>
        <conflict></conflict>
        <text>Replaced by new connection</text>
     </stream:error>
    '''
    def __init__(self,  text = None):
        super(StreamErrorConflictProtocolEntity, self).__init__("stream:error")
        self.setText(text)

    def setText(self, text = None):
        self.text = text or ''

    def toProtocolTreeNode(self):
        node = super(StreamErrorConflictProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("conflict"))
        node.addChild(ProtocolTreeNode("text", data=self.text))
        return node


    @staticmethod
    def fromProtocolTreeNode(node):
        return StreamErrorConflictProtocolEntity(node.getChild("text").getData())
