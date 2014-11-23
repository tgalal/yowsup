from .message_text import TextMessageProtocolEntity
from .message import MessageProtocolEntity
class TextMessageProtocolEntityFactory:
    @staticmethod
    def fromProtocolTreeNode(node):
        participant = node.getAttributeValue("participant")
        entityClass = GroupTextMessageProtocolEntity if participant else TextMessageProtocolEntity
        return entityClass.fromProtocolTreeNode(node)