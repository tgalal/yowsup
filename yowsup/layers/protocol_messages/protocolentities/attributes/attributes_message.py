from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_image import ImageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_extendedtext import ExtendedTextAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_document import DocumentAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_contact import ContactAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_location import LocationAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_video import VideoAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_audio import AudioAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_sticker import StickerAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_sender_key_distribution_message import \
    SenderKeyDistributionMessageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_protocol import ProtocolAttributes


class MessageAttributes(object):
    def __init__(
            self,
            conversation=None,
            image=None,
            contact=None,
            location=None,
            extended_text=None,
            document=None,
            audio=None,
            video=None,
            sticker=None,
            sender_key_distribution_message=None,
            protocol=None
    ):
        self._conversation = conversation  # type: str
        self._image = image  # type: ImageAttributes
        self._contact = contact  # type: ContactAttributes
        self._location = location  # type: LocationAttributes
        self._extended_text = extended_text  # type: ExtendedTextAttributes
        self._document = document  # type: DocumentAttributes
        self._audio = audio  # type: AudioAttributes
        self._video = video  # type: VideoAttributes
        self._sticker = sticker  # type: StickerAttributes
        self._sender_key_distribution_message = \
            sender_key_distribution_message  # type: SenderKeyDistributionMessageAttributes
        self._protocol = protocol  # type: ProtocolAttributes

    def __str__(self):
        attrs = []
        if self.conversation is not None:
            attrs.append(("conversation", self.conversation))
        if self.image is not None:
            attrs.append(("image", self.image))
        if self.contact is not None:
            attrs.append(("contact", self.contact))
        if self.location is not None:
            attrs.append(("location", self.location))
        if self.extended_text is not None:
            attrs.append(("extended_text", self.extended_text))
        if self.document is not None:
            attrs.append(("document", self.document))
        if self.audio is not None:
            attrs.append(("audio", self.audio))
        if self.video is not None:
            attrs.append(("video", self.video))
        if self.sticker is not None:
            attrs.append(("sticker", self.sticker))
        if self._sender_key_distribution_message is not None:
            attrs.append(("sender_key_distribution_message", self.sender_key_distribution_message))
        if self._protocol is not None:
            attrs.append(("protocol", self.protocol))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def conversation(self):
        return self._conversation

    @conversation.setter
    def conversation(self, value):
        self._conversation = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def contact(self):
        return self._contact

    @contact.setter
    def contact(self, value):
        self._contact = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def extended_text(self):
        return self._extended_text

    @extended_text.setter
    def extended_text(self, value):
        self._extended_text = value

    @property
    def document(self):
        return self._document

    @document.setter
    def document(self, value):
        self._document = value

    @property
    def audio(self):
        return self._audio

    @audio.setter
    def audio(self, value):
        self._audio = value

    @property
    def video(self):
        return self._video

    @video.setter
    def video(self, value):
        self._video = value

    @property
    def sticker(self):
        return self._sticker

    @sticker.setter
    def sticker(self, value):
        self._sticker = value

    @property
    def sender_key_distribution_message(self):
        return self._sender_key_distribution_message

    @sender_key_distribution_message.setter
    def sender_key_distribution_message(self, value):
        self._sender_key_distribution_message = value

    @property
    def protocol(self):
        return self._protocol

    @protocol.setter
    def protocol(self, value):
        self._protocol = value
