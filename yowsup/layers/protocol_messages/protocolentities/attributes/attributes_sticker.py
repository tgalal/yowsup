class StickerAttributes(object):
    def __init__(self, downloadablemedia_attributes, width, height, png_thumbnail=None):
        self._downloadablemedia_attributes = downloadablemedia_attributes
        self._width = width
        self._height = height
        self._png_thumbnail = png_thumbnail

    def __str__(self):
        attrs = []
        if self.width is not None:
            attrs.append(("width", self.width))
        if self.height is not None:
            attrs.append(("height", self.height))
        if self.png_thumbnail is not None:
            attrs.append(("png_thumbnail", self.png_thumbnail))
        attrs.append(("downloadable", self.downloadablemedia_attributes))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def downloadablemedia_attributes(self):
        return self._downloadablemedia_attributes

    @downloadablemedia_attributes.setter
    def downloadablemedia_attributes(self, value):
        self._downloadablemedia_attributes = value

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    @property
    def png_thumbnail(self):
        return self._png_thumbnail

    @png_thumbnail.setter
    def png_thumbnail(self, value):
        self._png_thumbnail = value
