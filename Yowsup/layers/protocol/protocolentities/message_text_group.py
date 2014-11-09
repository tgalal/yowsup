from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_text import TextMessageProtocolEntity
class GroupTextMessageProtocolEntity(TextMessageProtocolEntity):
    '''
    <message participant="{{PARTICIPANT_JID}}" 
        t="{{TIME_STAMP}}" from="{{GROUP_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <body>
            {{MESSAGE_DATA}}
        </body>
    </message>
    '''

    def __init__(self, _id, _from, participant, timestamp, notify, body, offline, retry = None):
        super(GroupTextMessageProtocolEntity, self).__init__("text", _id, _from, timestamp, notify, body, offline, retry)
        self.setPariticipant(participant)

    def setPariticipant(self, participant):
        self.participant = participant

    def toProtocolTreeNode(self):
        node = super(GroupTextMessageProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("participant", self.participant)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = TextMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GroupTextMessageProtocolEntity
        entity.setPariticipant(node.getAttributeValue("participant"))
        return entity
