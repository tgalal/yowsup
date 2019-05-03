class ExtendedTextAttributes(object):
    def __init__(self,
                 text, matched_text, canonical_url, description, title, jpeg_thumbnail
                 ):
        self._text = text
        self._matched_text = matched_text
        self._canonical_url = canonical_url
        self._description = description
        self._title = title
        self._jpeg_thumbnail = jpeg_thumbnail

    @property
    def text(self):
        return self._text

    @property
    def matched_text(self):
        return self._matched_text

    @property
    def canonical_url(self):
        return self._canonical_url

    @property
    def description(self):
        return self._description

    @property
    def title(self):
        return self._title

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail
