from .message import MessageProtocolEntity
from .proto import ProtoProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
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
    def __init__(self, messageType, messageAttributes):
        super(ProtomessageProtocolEntity, self).__init__(messageType, messageAttributes)
        self._proto = Message()

    def __str__(self):
        out = super(ProtomessageProtocolEntity, self).__str__()
        return "%s\nproto=%s" % (out, self._proto)

    @property
    def proto(self):
        return self._proto

    def deserializeProtoData(self, protoData):
        m = Message()
        m.ParseFromString(protoData)
        return m

    def toProtocolTreeNode(self):
        node = super(ProtomessageProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtoProtocolEntity(self._proto.SerializeToString()).toProtocolTreeNode())

        return node

    def setProtoFromData(self, protoData):
        self._proto = self.deserializeProtoData(protoData)

    @classmethod
    def fromProtocolTreeNode(cls, node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__= cls
        entity.setProtoFromData(node.getChild("proto").getData())
        return entity