from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from .message_media import MediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_contact import ContactAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class ContactMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    def __init__(self, contact_attrs, message_meta_attrs):
        # type: (ContactAttributes, MessageMetaAttributes) -> None
        super(ContactMediaMessageProtocolEntity, self).__init__(
            "contact", MessageAttributes(contact=contact_attrs), message_meta_attrs
        )

    @property
    def media_specific_attributes(self):
        return self.message_attributes.contact

    @property
    def display_name(self):
        return self.media_specific_attributes.display_name

    @display_name.setter
    def display_name(self, value):
        self.media_specific_attributes.display_name = value

    @property
    def vcard(self):
        return self.media_specific_attributes.vcard

    @vcard.setter
    def vcard(self, value):
        self.media_specific_attributes.vcard = value
