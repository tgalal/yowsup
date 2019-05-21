from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_sticker import StickerAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class StickerDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    def __init__(self, sticker_attrs, message_meta_attrs):
        # type: (StickerAttributes, MessageMetaAttributes) -> None
        super(StickerDownloadableMediaMessageProtocolEntity, self).__init__(
            "sticker", MessageAttributes(sticker=sticker_attrs),  message_meta_attrs
        )

    @property
    def media_specific_attributes(self):
        return self.message_attributes.sticker

    @property
    def downloadablemedia_specific_attributes(self):
        return self.message_attributes.sticker.downloadablemedia_attributes

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
    def png_thumbnail(self):
        return self.media_specific_attributes.png_thumbnail

    @png_thumbnail.setter
    def png_thumbnail(self, value):
        self.media_specific_attributes.png_thumbnail = value
