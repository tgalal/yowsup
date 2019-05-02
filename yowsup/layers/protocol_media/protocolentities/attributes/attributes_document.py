class DocumentAttributes(object):
    def __init__(self, file_name, file_length, title=None, page_count=None, jpeg_thumbnail=None):
        self._file_name = file_name
        self._file_length = file_length
        self._title = title
        self._page_count = page_count
        self._jpeg_thumbnail = jpeg_thumbnail

    @property
    def file_name(self):
        return self._file_name

    @property
    def file_length(self):
        return self._file_length

    @property
    def title(self):
        return self._title

    @property
    def page_count(self):
        return self._page_count

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail
