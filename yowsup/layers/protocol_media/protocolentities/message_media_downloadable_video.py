from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_video import VideoAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class VideoDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, video_attrs, message_meta_attrs):
        # type: (VideoAttributes, MessageMetaAttributes) -> None
        super(VideoDownloadableMediaMessageProtocolEntity, self).__init__(
            "video", MessageAttributes(video=video_attrs), message_meta_attrs
        )

    @property
    def media_specific_attributes(self):
        return self.message_attributes.video

    @property
    def downloadablemedia_specific_attributes(self):
        return self.message_attributes.video.downloadablemedia_attributes

    @property
    def width(self):
        return self.media_specific_attributes.width

    @width.setter
    def width(self, value):
        self.media_specific_attributes.width = value

    @property
    def height(self):
        return self.media_specific_attributes.height

    @height.setter
    def height(self, value):
        self.media_specific_attributes.height = value

    @property
    def seconds(self):
        return self.media_specific_attributes.seconds

    @seconds.setter
    def seconds(self, value):
        self.media_specific_attributes.seconds = value

    @property
    def gif_playback(self):
        return self.media_specific_attributes.gif_playback

    @gif_playback.setter
    def gif_playback(self, value):
        self.media_specific_attributes.gif_playback = value

    @property
    def jpeg_thumbnail(self):
        return self.media_specific_attributes.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.media_specific_attributes.jpeg_thumbnail = value

    @property
    def caption(self):
        return self.media_specific_attributes.caption

    @caption.setter
    def caption(self, value):
        self.media_specific_attributes.caption = value

    @property
    def gif_attribution(self):
        return self.proto.gif_attribution

    @gif_attribution.setter
    def gif_attribution(self, value):
        self.media_specific_attributes.gif_attributions = value

    @property
    def streaming_sidecar(self):
        return self.media_specific_attributes.streaming_sidecar

    @streaming_sidecar.setter
    def streaming_sidecar(self, value):
        self.media_specific_attributes.streaming_sidecar = value
