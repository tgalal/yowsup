from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_downloadablemedia import \
    DownloadableMediaMessageAttributes


class AudioAttributes(object):
    def __init__(self, downloadablemedia_attributes, seconds, ptt, streaming_sidecar=None):
        # type: (DownloadableMediaMessageAttributes, int, bool, bytes) -> None
        """
        :param seconds: duration of audio playback in seconds
        :param ptt: indicates whether this is a push-to-talk audio message
        :param streaming_sidecar
        """
        self._downloadablemedia_attributes = downloadablemedia_attributes
        self._seconds = seconds  # type: int
        self._ptt = ptt  # type: bool
        self._streaming_sidecar = streaming_sidecar  # type: bytes

    def __str__(self):
        attrs = []
        if self.seconds is not None:
            attrs.append(("seconds", self.seconds))
        if self.ptt is not None:
            attrs.append(("ptt", self.ptt))
        if self._streaming_sidecar is not None:
            attrs.append(("streaming_sidecar", "[binary data]"))
        attrs.append(("downloadable", self.downloadablemedia_attributes))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def downloadablemedia_attributes(self):
        return self._downloadablemedia_attributes

    @downloadablemedia_attributes.setter
    def downloadablemedia_attributes(self, value):
        self._downloadablemedia_attributes = value

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value):
        self._seconds = value

    @property
    def ptt(self):
        return self._ptt

    @ptt.setter
    def ptt(self, value):
        self._ptt = value

    @property
    def streaming_sidecar(self):
        return self._streaming_sidecar

    @streaming_sidecar.setter
    def streaming_sidecar(self, value):
        self._streaming_sidecar = value
