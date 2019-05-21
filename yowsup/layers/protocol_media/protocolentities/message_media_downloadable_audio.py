from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_audio \
    import AudioAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes


class AudioDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, audio_attrs, downloadablemedia_attrs, message_meta_attrs):
        """
        :type audio_attrs: AudioAttributes
        :type downloadablemedia_attrs: DownloadableMediaMessageAttributes
        :type message_meta_attrs: MessageMetaAttributes
        """
        super(AudioDownloadableMediaMessageProtocolEntity, self).__init__(
            "audio", downloadablemedia_attrs, message_meta_attrs
        )
        self.seconds = audio_attrs.seconds
        self.ptt = audio_attrs.ptt

    @property
    def proto(self):
        return self._proto.audio_message

    @property
    def seconds(self):
        return self.proto.seconds

    @seconds.setter
    def seconds(self, value):
        """
        :type value: int
        """
        self.proto.seconds = value

    @property
    def ptt(self):
        return self.proto.ptt

    @ptt.setter
    def ptt(self, value):
        """
        :type value: bool
        """
        self.proto.ptt = value
