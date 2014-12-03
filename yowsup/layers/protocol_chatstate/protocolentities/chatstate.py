from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ChatstateProtocolEntity(ProtocolEntity):

    '''
    INCOMING

    <chatstate from="xxxxxxxxxxx@s.whatsapp.net">
    <{{composing|paused}}></{{composing|paused}}>
    </chatstate>

    OUTGOING

    <chatstate to="xxxxxxxxxxx@s.whatsapp.net">
    <{{composing|paused}}></{{composing|paused}}>
    </chatstate>
    '''

    def __init__(self, _state):
        super(ChatstateProtocolEntity, self).__init__("chatstate")
        self._state = _state

    def getState(self):
        return self._state

    def toProtocolTreeNode(self):
        node = self._createProtocolTreeNode({}, None, data = None)
        node.addChild(ProtocolTreeNode(self._state))
        return node

    def __str__(self):
        out  = "CHATSTATE:\n"
        out += "State: %s\n" % self._state
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return ChatstateProtocolEntity(
            node.getAllChildren()[0].tag,
            )
