from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_media.protocolentities.attributes.attributes_sticker import StickerAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes


class StickerDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, sticker_attrs, downloadablemedia_attrs, message_meta_attrs):
        # type: (StickerAttributes, DownloadableMediaMessageAttributes, MessageMetaAttributes) -> None
        super(StickerDownloadableMediaMessageProtocolEntity, self).__init__(
            "sticker", downloadablemedia_attrs, message_meta_attrs
        )
        self.width = sticker_attrs.width
        self.height = sticker_attrs.height

        if sticker_attrs.png_thumbnail is not None:
            self.png_thumbnail = sticker_attrs.png_thumbnail

    @property
    def proto(self):
        return self._proto.sticker_message

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
    def png_thumbnail(self):
        return self.proto.png_thumbnail

    @png_thumbnail.setter
    def png_thumbnail(self, value):
        self.proto.png_thumbnail = value if value is not None else b""
