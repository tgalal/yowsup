from yowsup.layers.protocol_messages.protocolentities.protomessage import ProtomessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_media import MediaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes

import logging
logger = logging.getLogger(__name__)


class MediaMessageProtocolEntity(ProtomessageProtocolEntity):
    TYPE_MEDIA_IMAGE = "image"
    TYPE_MEDIA_VIDEO = "video"
    TYPE_MEDIA_AUDIO = "audio"
    TYPE_MEDIA_CONTACT = "contact"
    TYPE_MEDIA_LOCATION = "location"
    TYPE_MEDIA_DOCUMENT = "document"
    TYPE_MEDIA_GIF = "gif"
    TYPE_MEDIA_PTT = "ptt"
    TYPE_MEDIA_URL = "url"

    TYPES_MEDIA = (
        TYPE_MEDIA_IMAGE, TYPE_MEDIA_AUDIO, TYPE_MEDIA_VIDEO,
        TYPE_MEDIA_CONTACT, TYPE_MEDIA_LOCATION, TYPE_MEDIA_DOCUMENT,
        TYPE_MEDIA_GIF, TYPE_MEDIA_PTT, TYPE_MEDIA_URL
    )

    def __init__(self, media_type, media_message_attrs, message_attrs):
        """
        :type media_type: str
        :type media_message_attrs: MediaAttributes
        :type message_attrs: MessageAttributes
        """
        super(MediaMessageProtocolEntity, self).__init__("media", message_attrs)
        self.media_type = media_type  # type: str

        if media_message_attrs.context_info:
            self.context_stanza_id = media_message_attrs.context_info.stanza_id
            self.context_participant = media_message_attrs.context_info.participant
            self.context_quoted_message = media_message_attrs.context_info.quoted_message
            self.context_edit_version = media_message_attrs.context_info.edit_version
            self.context_remote_jid = media_message_attrs.context_info.remote_jid
            self.context_mentioned_jid = media_message_attrs.context_info.mentioned_jid
            self.context_revoke_message = media_message_attrs.context_info.revoke_message

    def __str__(self):
        out = super(MediaMessageProtocolEntity, self).__str__()
        out += "\nmediatype=%s" % self.media_type
        return out

    @property
    def context_stanza_id(self):
        return self.proto.stanza_id

    @context_stanza_id.setter
    def context_stanza_id(self, value):
        self.proto.context_info.stanza_id = value

    @property
    def context_participant(self):
        return self.proto.context_info.participant

    @context_participant.setter
    def context_participant(self, value):
        self.proto.context_info = value

    @property
    def context_quoted_message(self):
        return self.proto.context_info.quoted_message

    @context_quoted_message.setter
    def context_quoted_message(self, value):
        self.proto.context_info.quoted_message = value

    @property
    def context_edit_version(self):
        return self.proto.context_info.edit_version

    @context_edit_version.setter
    def context_edit_version(self, value):
        self.proto.context_info.edit_version = value

    @property
    def context_remote_jid(self):
        return self.proto.context_info.remote_jid

    @context_remote_jid.setter
    def context_remote_jid(self, value):
        self.proto.context_info.remote_jid = value

    @property
    def context_mentioned_jid(self):
        return self.proto.context_info.mentioned_jid

    @context_mentioned_jid.setter
    def context_mentioned_jid(self, value):
        self.proto.context_info.mentioned_jid = value

    @property
    def context_revoke_message(self):
        return self.proto.context_info.revoke_message

    @context_revoke_message.setter
    def context_revoke_message(self, value):
        self.proto.context_info.revoke_message = value

    @property
    def media_type(self):
        return self._media_type

    @media_type.setter
    def media_type(self, value):
        if value not in MediaMessageProtocolEntity.TYPES_MEDIA:
            logger.warn("media type: '%s' is not supported" % value)
        self._media_type = value

    def toProtocolTreeNode(self):
        node = super(MediaMessageProtocolEntity, self).toProtocolTreeNode()
        protoNode = node.getChild("proto")
        protoNode["mediatype"] = self.media_type
        return node

    @classmethod
    def fromProtocolTreeNode(cls, node):
        entity = ProtomessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = cls
        entity.media_type = node.getChild("proto")["mediatype"]
        return entity
