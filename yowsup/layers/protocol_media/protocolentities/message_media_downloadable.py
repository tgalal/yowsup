from .message_media import MediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes


class DownloadableMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    def __init__(self, media_type, downloadable_media_message_attrs, message_attrs):
        """
        :type media_type: str
        :type downloadable_media_message_attrs: DownloadableMediaMessageAttributes
        :type message_attrs: MessageAttributes
        """
        super(DownloadableMediaMessageProtocolEntity, self).__init__(
            media_type, downloadable_media_message_attrs, message_attrs
        )

    @property
    def url(self):
        return self.proto.url

    @url.setter
    def url(self, value):
        self.proto.url = value

    @property
    def mimetype(self):
        return self.proto.mimetype

    @mimetype.setter
    def mimetype(self, value):
        self.proto.mimetype = value

    @property
    def file_sha256(self):
        return self.proto.file_sha256

    @file_sha256.setter
    def file_sha256(self, value):
        self.proto.file_sha256 = value

    @property
    def file_length(self):
        return self.proto.file_length

    @file_length.setter
    def file_length(self, value):
        self.proto.file_length = value

    @property
    def media_key(self):
        return self.proto.media_key

    @media_key.setter
    def media_key(self, value):
        self.proto.media_key = value
