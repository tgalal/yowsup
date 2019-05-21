from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_image import ImageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class ImageDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, image_attrs, message_meta_attrs):
        # type: (ImageAttributes, MessageMetaAttributes) -> None
        super(ImageDownloadableMediaMessageProtocolEntity, self).__init__(
            "image", MessageAttributes(image=image_attrs), message_meta_attrs
        )

    @property
    def media_specific_attributes(self):
        return self.message_attributes.image

    @property
    def downloadablemedia_specific_attributes(self):
        return self.message_attributes.image.downloadablemedia_attributes

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
    def jpeg_thumbnail(self):
        return self.media_specific_attributes.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.media_specific_attributes.jpeg_thumbnail = value if value is not None else b""

    @property
    def caption(self):
        return self.media_specific_attributes.caption

    @caption.setter
    def caption(self, value):
        self.media_specific_attributes.caption = value if value is not None else ""
