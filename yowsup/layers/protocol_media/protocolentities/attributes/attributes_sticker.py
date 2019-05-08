class StickerAttributes(object):
    def __init__(self, width, height, png_thumbnail=None):
        self._width = width
        self._height = height
        self._png_thumbnail = png_thumbnail

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def png_thumbnail(self):
        return self._png_thumbnail
