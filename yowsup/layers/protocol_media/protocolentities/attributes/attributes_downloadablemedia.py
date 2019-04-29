from yowsup.layers.protocol_media.protocolentities.attributes.attributes_media import MediaAttributes


class DownloadableMediaMessageAttributes(MediaAttributes):
    def __init__(self, url, mimetype, length, sha256, media_key, context_info=None):
        super(DownloadableMediaMessageAttributes, self).__init__(context_info)
        self._url = url
        self._mimetype = mimetype
        self._length = length
        self._sha256 = sha256
        self._media_key = media_key
