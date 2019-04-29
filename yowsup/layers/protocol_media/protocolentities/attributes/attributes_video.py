class VideoAttributes(object):
    def __init__(self, width, height, seconds,
                 gif_playback=None, jpeg_thumbnail=None, gif_attribution=None, caption=None, streaming_sidecar=None):
        self._width = width
        self._height = height
        self._seconds = seconds
        self._gif_playback = gif_playback,
        self._jpeg_thumbnail = jpeg_thumbnail
        self._gif_attribution = gif_attribution
        self._caption = caption
        self._streaming_sidecar = streaming_sidecar

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def seconds(self):
        return self._seconds

    @property
    def gif_playback(self):
        return self._gif_playback

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail

    @property
    def gif_attribution(self):
        return self._gif_attribution

    @property
    def caption(self):
        return self._caption

    @property
    def streaming_sidecar(self):
        return self._streaming_sidecar
