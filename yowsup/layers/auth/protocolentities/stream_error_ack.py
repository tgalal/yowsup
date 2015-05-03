from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class StreamErrorAckProtocolEntity(ProtocolEntity):
    '''
     <stream:error>
        <ack></ack>
     </stream:error>
    '''
    def __init__(self):
        super(StreamErrorAckProtocolEntity, self).__init__("stream:error")

    def toProtocolTreeNode(self):
        node = super(StreamErrorAckProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("ack"))
        return node

    def __str__(self):
        out = "Ack Stream Error\n"
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return StreamErrorAckProtocolEntity()
