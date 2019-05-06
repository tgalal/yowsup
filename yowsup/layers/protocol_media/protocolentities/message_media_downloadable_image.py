from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_image import ImageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class ImageDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, image_attrs, downloadablemedia_attrs, message_attrs):
        # type: (ImageAttributes, DownloadableMediaMessageAttributes, MessageAttributes) -> None
        super(ImageDownloadableMediaMessageProtocolEntity, self).__init__(
            "image", downloadablemedia_attrs, message_attrs
        )
        self.width = image_attrs.width
        self.height = image_attrs.height
        self.caption = image_attrs.caption
        self.jpeg_thumbnail = image_attrs.jpeg_thumbnail

    @property
    def proto(self):
        return self._proto.image_message

    @property
    def width(self):
        return self.proto.width

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
    def jpeg_thumbnail(self):
        return self.proto.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.jpeg_thumbnail = value if value is not None else b""

    @property
    def caption(self):
        return self.proto.caption

    @caption.setter
    def caption(self, value):
        self.proto.caption = value if value is not None else ""
