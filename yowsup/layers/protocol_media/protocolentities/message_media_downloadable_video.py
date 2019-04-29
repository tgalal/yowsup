from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_video import VideoAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class VideoDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, video_attrs, downloadablemedia_attrs, message_attrs):
        """
        :type video_attrs: VideoAttributes
        :type downloadablemedia_attrs: DownloadableMediaMessageAttributes
        :type message_attrs: MessageAttributes
        """
        super(VideoDownloadableMediaMessageProtocolEntity, self).__init__(
            "video", downloadablemedia_attrs, message_attrs
        )
        self.width = video_attrs.width
        self.height = video_attrs.height
        self.seconds = video_attrs.seconds
        self.caption = video_attrs.caption
        self.gif_playback = video_attrs.gif_playback
        self.jpeg_thumbnail = video_attrs.jpeg_thumbnail
        self.gif_attribution = video_attrs.gif_attribution
        self.streaming_sidecar = video_attrs.streaming_sidecar

    @property
    def proto(self):
        return self._proto.video_message

    @property
    def width(self):
        return self._proto.width

    @width.setter
    def width(self, value):
        self.proto.width = value

    @property
    def height(self):
        return self.proto.height

    @height.setter
    def height(self, value):
        self.proto.height = value

    @property
    def seconds(self):
        return self.proto.seconds

    @seconds.setter
    def seconds(self, value):
        self.proto.seconds = value

    @property
    def gif_playback(self):
        return self.proto.gif_playback

    @gif_playback.setter
    def gif_playback(self, value):
        self.proto.gif_playback = value

    @property
    def jpeg_thumbnail(self):
        return self._proto.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.jpeg_thumbnail = value

    @property
    def caption(self):
        return self.proto.caption

    @caption.setter
    def caption(self, value):
        self.proto.caption = value

    @property
    def gif_attribution(self):
        return self.proto.gif_attribution

    @gif_attribution.setter
    def gif_attribution(self, value):
        self.proto.gif_attributions = value

    @property
    def streaming_sidecar(self):
        return self.proto.streaming_sidecar

    @streaming_sidecar.setter
    def streaming_sidecar(self, value):
        self.proto.streaming_sidecar = value
