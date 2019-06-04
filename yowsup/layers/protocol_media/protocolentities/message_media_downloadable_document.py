from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_document import DocumentAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class DocumentDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, document_attrs, message_meta_attrs):
        """
        :type document_attrs: DocumentAttributes
        :type message_meta_attrs: MessageMetaAttributes
        """
        super(DocumentDownloadableMediaMessageProtocolEntity, self).__init__(
            "document", MessageAttributes(document=document_attrs), message_meta_attrs
        )

    @property
    def media_specific_attributes(self):
        return self.message_attributes.document

    @property
    def downloadablemedia_specific_attributes(self):
        return self.message_attributes.document.downloadablemedia_attributes

    @property
    def file_name(self):
        return self.media_specific_attributes.file_name

    @file_name.setter
    def file_name(self, value):
        self.media_specific_attributes.file_name = value

    @property
    def file_length(self):
        return self.media_specific_attributes.file_length

    @file_length.setter
    def file_length(self, value):
        self.media_specific_attributes.file_length = value

    @property
    def title(self):
        return self.media_specific_attributes.title

    @title.setter
    def title(self, value):
        self.media_specific_attributes.title = value

    @property
    def page_count(self):
        return self.media_specific_attributes.page_count

    @page_count.setter
    def page_count(self, value):
        self.media_specific_attributes.page_count = value

    @property
    def jpeg_thumbnail(self):
        return self.media_specific_attributes.image_message.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.media_specific_attributes.image_message.jpeg_thumbnail = value
