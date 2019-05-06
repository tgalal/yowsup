from yowsup.layers.protocol_media.protocolentities.attributes.attributes_media import MediaAttributes


class DownloadableMediaMessageAttributes(MediaAttributes):
    def __init__(self, mimetype, file_length, file_sha256, url=None, media_key=None, context_info=None):
        super(DownloadableMediaMessageAttributes, self).__init__(context_info)
        self._mimetype = mimetype
        self._file_length = file_length
        self._file_sha256 = file_sha256
        self._url = url
        self._media_key = media_key

    def __str__(self):
        return "[url=%s, mimetype=%s, file_length=%d, file_sha256=%s, media_key=%s]" % (
            self.url,self.mimetype, self.file_length, base64.b64encode(self.file_sha256),
            base64.b64encode(self.media_key)
        )

    @property
    def url(self):
        return self._url

    @property
    def mimetype(self):
        return self._mimetype

    @property
    def file_length(self):
        return self._file_length

    @property
    def file_sha256(self):
        return self._file_sha256

    @property
    def media_key(self):
        return self._media_key

