from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_document \
    import DocumentAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class DocumentDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, document_attrs, downloadablemedia_attrs, message_attrs):
        """
        :type document_attrs: DocumentAttributes
        :type downloadablemedia_attrs: DownloadableMediaMessageAttributes
        :type message_attrs: MessageAttributes
        """
        super(DocumentDownloadableMediaMessageProtocolEntity, self).__init__(
            "document", downloadablemedia_attrs, message_attrs
        )
        self.file_name = document_attrs.file_name
        self.file_length = document_attrs.file_length
        self.title = document_attrs.title
        self.page_count = document_attrs.page_count
        self.jpeg_thumbnail = document_attrs.jpeg_thumbnail

    @property
    def proto(self):
        return self._proto.document_message

    @property
    def file_name(self):
        return self.proto.file_name

    @file_name.setter
    def file_name(self, value):
        self.proto.file_name = value

    @property
    def file_length(self):
        return self.proto.file_length

    @file_length.setter
    def file_length(self, value):
        self.proto.file_length = value

    @property
    def title(self):
        return self.proto.title

    @title.setter
    def title(self, value):
        self.proto.title = value

    @property
    def page_count(self):
        return self.proto.page_count

    @page_count.setter
    def page_count(self, value):
        self.proto.page_count = value

    @property
    def jpeg_thumbnail(self):
        return self.proto.image_message.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.image_message.jpeg_thumbnail = value
