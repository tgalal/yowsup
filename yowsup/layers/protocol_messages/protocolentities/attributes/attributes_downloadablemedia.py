from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_media import MediaAttributes
from yowsup.common.tools import MimeTools
import base64
import hashlib
import os


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
            self.url,self.mimetype, self.file_length, base64.b64encode(self.file_sha256) if self.file_sha256 else None,
            base64.b64encode(self.media_key) if self.media_key else None
        )

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def mimetype(self):
        return self._mimetype

    @mimetype.setter
    def mimetype(self, value):
        self._mimetype = value

    @property
    def file_length(self):
        return self._file_length

    @file_length.setter
    def file_length(self, value):
        self._file_length = value

    @property
    def file_sha256(self):
        return self._file_sha256

    @file_sha256.setter
    def file_sha256(self, value):
        self._file_sha256 = value

    @property
    def media_key(self):
        return self._media_key

    @media_key.setter
    def media_key(self, value):
        self._media_key = value

    @staticmethod
    def from_file(
            filepath, mimetype=None, file_length=None,
            file_sha256=None, url=None, media_key=None, context_info=None
    ):
        mimetype = MimeTools.getMIME(filepath) if mimetype is None else mimetype
        file_length = os.path.getsize(filepath) if file_length is None else file_length
        if file_sha256 is None:
            with open(filepath, 'rb') as f:
                file_sha256 = hashlib.sha256(f.read()).digest()
        return DownloadableMediaMessageAttributes(
            mimetype, file_length, file_sha256, url, media_key, context_info
        )
