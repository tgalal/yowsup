from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from .message_media import MediaMessageProtocolEntity
from .attributes.attributes_contact import ContactAttributes
from .attributes.attributes_media import MediaAttributes


class ContactMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    def __init__(self, contact_attrs, media_attrs, message_attrs):
        # type: (ContactAttributes, MediaAttributes, MessageAttributes) -> None
        super(ContactMediaMessageProtocolEntity, self).__init__("contact", media_attrs, message_attrs)
        self.display_name = contact_attrs.display_name
        self.vcard = contact_attrs.vcard

    @property
    def proto(self):
        return self._proto.contact_message

    @property
    def display_name(self):
        return self.proto.display_name

    @display_name.setter
    def display_name(self, value):
        self.proto.display_name = value

    @property
    def vcard(self):
        return self.proto.vcard

    @vcard.setter
    def vcard(self, value):
        self.proto.vcard = value
