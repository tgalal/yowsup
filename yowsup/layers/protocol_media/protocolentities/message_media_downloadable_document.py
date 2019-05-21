from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes


class DocumentDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, document_attrs, downloadablemedia_attrs, message_meta_attrs):
        """
        :type document_attrs: DocumentAttributes
        :type downloadablemedia_attrs: DownloadableMediaMessageAttributes
        :type message_meta_attrs: MessageMetaAttributes
        """
        super(DocumentDownloadableMediaMessageProtocolEntity, self).__init__(
            "document", downloadablemedia_attrs, message_meta_attrs
        )
        self.file_name = document_attrs.file_name
        self.file_length = document_attrs.file_length
        if document_attrs.title is not None:
            self.title = document_attrs.title
        if document_attrs.page_count is not None:
            self.page_count = document_attrs.page_count
        if document_attrs.jpeg_thumbnail is not None:
            self.jpeg_thumbnail = document_attrs.jpeg_thumbnail

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
