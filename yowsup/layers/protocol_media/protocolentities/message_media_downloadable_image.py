from .message_media_downloadable import DownloadableMediaMessageProtocolEntity


class ImageDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, image_attrs, downloadablemdia_attrs, message_attrs):
        super(ImageDownloadableMediaMessageProtocolEntity, self).__init__(
            "image", downloadablemdia_attrs, message_attrs
        )
        self.width = image_attrs.width
        self.height = image_attrs.height
        self.caption = image_attrs.caption
        self.jpeg_thumbnail = image_attrs.jpegThumbnail

    @property
    def proto(self):
        return self._proto.image_message

    @property
    def width(self):
        return self.proto.image_message.width

    @width.setter
    def width(self, value):
        self.proto.image_message.width = value

    @property
    def height(self):
        return self.proto.image_message.height

    @height.setter
    def height(self, value):
        self.proto.image_message.height = value

    @property
    def jpeg_thumbnail(self):
        return self.proto.image_message.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.image_message.jpeg_thumbnail = value

    @property
    def caption(self):
        return self.proto.image_message.caption

    @caption.setter
    def caption(self, value):
        self.proto.image_message.caption = value
