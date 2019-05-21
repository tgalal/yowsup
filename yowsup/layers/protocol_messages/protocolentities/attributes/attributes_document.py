from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_downloadablemedia import \
    DownloadableMediaMessageAttributes
import os


class DocumentAttributes(object):
    def __init__(self, downloadablemedia_attributes, file_name, file_length, title=None, page_count=None, jpeg_thumbnail=None):
        self._downloadablemedia_attributes = downloadablemedia_attributes
        self._file_name = file_name
        self._file_length = file_length
        self._title = title
        self._page_count = page_count
        self._jpeg_thumbnail = jpeg_thumbnail

    def __str__(self):
        attrs = []
        if self.file_name is not None:
            attrs.append(("file_name", self.file_name))
        if self.file_length is not None:
            attrs.append(("file_length", self.file_length))
        if self.title is not None:
            attrs.append(("title", self.title))
        if self.page_count is not None:
            attrs.append(("page_count", self.page_count))
        if self.jpeg_thumbnail is not None:
            attrs.append(("jpeg_thumbnail", self.jpeg_thumbnail))
        attrs.append(("downloadable", self.downloadablemedia_attributes))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def downloadablemedia_attributes(self):
        return self._downloadablemedia_attributes

    @downloadablemedia_attributes.setter
    def downloadablemedia_attributes(self, value):
        self._downloadablemedia_attributes = value

    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    @property
    def file_length(self):
        return self._file_length

    @file_length.setter
    def file_length(self, value):
        self._file_length = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, value):
        self._page_count = value

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self._jpeg_thumbnail = value

    @staticmethod
    def from_filepath(filepath):
        return DocumentAttributes(
            DownloadableMediaMessageAttributes.from_file(filepath),
            os.path.basename(filepath),
            os.path.getsize(filepath)
        )
