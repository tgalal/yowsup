from .message import MessageProtocolEntity
from .proto import ProtoProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.converter import AttributesConverter
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
import logging

logger = logging.getLogger(__name__)


class ProtomessageProtocolEntity(MessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}"
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
            <proto>
                {{SERIALIZE_PROTO_DATA}}
            </proto>
    </message>
    '''
    def __init__(self, messageType, message_attributes, messageMetaAttributes):
        super(ProtomessageProtocolEntity, self).__init__(messageType, messageMetaAttributes)
        self._message_attributes = message_attributes  # type: MessageAttributes

    def __str__(self):
        out = super(ProtomessageProtocolEntity, self).__str__()
        return "%s\nmessage_attributes=%s" % (out, self._message_attributes)

    def toProtocolTreeNode(self):
        node = super(ProtomessageProtocolEntity, self).toProtocolTreeNode()
        node.addChild(
            ProtoProtocolEntity(
                AttributesConverter.get().message_to_protobytes(self._message_attributes)
            ).toProtocolTreeNode()
        )
        return node

    @property
    def message_attributes(self):
        return self._message_attributes

    @message_attributes.setter
    def message_attributes(self, value):
        self._message_attributes = value

    @classmethod
    def fromProtocolTreeNode(cls, node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = cls
        m = Message()
        m.ParseFromString(node.getChild("proto").getData())
        entity.message_attributes = AttributesConverter.get().proto_to_message(m)
        return entity
