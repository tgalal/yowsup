class ExtendedTextAttributes(object):
    def __init__(
            self,
            text, matched_text, canonical_url, description, title, jpeg_thumbnail, context_info
    ):
        self._text = text
        self._matched_text = matched_text
        self._canonical_url = canonical_url
        self._description = description
        self._title = title
        self._jpeg_thumbnail = jpeg_thumbnail
        self._context_info = context_info

    def __str__(self):
        attrs = []
        if self.text is not None:
            attrs.append(("text", self.text))
        if self.matched_text is not None:
            attrs.append(("matched_text", self.matched_text))
        if self.canonical_url is not None:
            attrs.append(("canonical_url", self.canonical_url))
        if self.description is not None:
            attrs.append(("description", self.description))
        if self.title is not None:
            attrs.append(("title", self.title))
        if self.jpeg_thumbnail is not None:
            attrs.append(("jpeg_thumbnail", "[binary data]"))
        if self.context_info is not None:
            attrs.append(("context_info", self.context_info))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def matched_text(self):
        return self._matched_text

    @matched_text.setter
    def matched_text(self, value):
        self._matched_text = value

    @property
    def canonical_url(self):
        return self._canonical_url

    @canonical_url.setter
    def canonical_url(self, value):
        self._canonical_url = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self._jpeg_thumbnail = value

    @property
    def context_info(self):
        return self._context_info

    @context_info.setter
    def context_info(self, value):
        self._context_info = value
