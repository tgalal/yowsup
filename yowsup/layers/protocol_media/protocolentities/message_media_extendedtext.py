from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from .message_media import MediaMessageProtocolEntity
from .attributes.attributes_extendedtext import ExtendedTextAttributes
from .attributes.attributes_media import MediaAttributes


class ExtendedTextMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    def __init__(self, extended_text_attrs, media_attrs, message_attrs):
        # type: (ExtendedTextAttributes, MediaAttributes, MessageAttributes) -> None
        super(ExtendedTextMediaMessageProtocolEntity, self).__init__("url", media_attrs, message_attrs)
        self.text = extended_text_attrs.text
        self.matched_text = extended_text_attrs.matched_text
        self.canonical_url = extended_text_attrs.canonical_url
        self.description = extended_text_attrs.description
        self.title = extended_text_attrs.title
        self.jpeg_thumbnail = extended_text_attrs.jpeg_thumbnail

    @property
    def proto(self):
        return self._proto.extended_text_message

    @property
    def text(self):
        return self.proto.text

    @text.setter
    def text(self, value):
        self.proto.text = value

    @property
    def matched_text(self):
        return self.proto.matched_text

    @matched_text.setter
    def matched_text(self, value):
        self.proto.matched_text = value

    @property
    def canonical_url(self):
        return self.proto.canonical_url

    @canonical_url.setter
    def canonical_url(self, value):
        self.proto.canonical_url = value

    @property
    def description(self):
        return self.proto.description

    @description.setter
    def description(self, value):
        self.proto.description = value

    @property
    def title(self):
        return self.proto.title

    @title.setter
    def title(self, value):
        self.proto.title = value

    @property
    def jpeg_thumbnail(self):
        return self.proto.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.jpeg_thumbnail = value
