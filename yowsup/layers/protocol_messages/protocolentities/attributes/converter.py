from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_image import ImageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_downloadablemedia \
    import DownloadableMediaMessageAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_media import MediaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_context_info import ContextInfoAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from yowsup.layers.protocol_messages.proto.e2e_pb2 import ContextInfo
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_extendedtext import ExtendedTextAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_document import DocumentAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_contact import ContactAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_location import LocationAttributes


class AttributesConverter(object):

    __instance = None

    @classmethod
    def get(cls):
        if cls.__instance is None:
            cls.__instance = AttributesConverter()
        return cls.__instance

    def contact_to_proto(self, contact_attributes):
        # type: (ContactAttributes) -> Message.ContactMessage
        contact_message = Message.ContactMessage()
        contact_message.display_name = contact_attributes.display_name
        contact_message.vcard = contact_attributes.vcard
        contact_message.context_info = self.contextinfo_to_proto(contact_attributes.context_info)
        return contact_message

    def proto_to_contact(self, proto):
        # type: (Message.ContactMessage) -> ContactAttributes
        return ContactAttributes(
            proto.display_name,
            proto.vcard,
            self.proto_to_contextinfo(proto.context_info) if proto.HasField("context_info") else None
        )

    def location_to_proto(self, location_attributes):
        # type: (LocationAttributes) -> Message.LocationMessage
        location_message = Message.LocationMessage()
        location_message._degrees_latitude = location_attributes.degrees_latitude
        location_message._degrees_longitude = location_attributes.degrees_longitude
        location_message._name = location_attributes.name
        location_message._address = location_attributes.address
        location_message._url = location_attributes.url
        location_message._duration = location_attributes.duration
        location_message._accuracy_in_meters = location_attributes.accuracy_in_meters
        location_message._speed_in_mps = location_attributes.speed_in_mps
        location_message._degrees_clockwise_from_magnetic_north = \
            location_attributes.degrees_clockwise_from_magnetic_north
        location_message._axolotl_sender_key_distribution_message = \
            location_attributes.axolotl_sender_key_distribution_message
        location_message._jpeg_thumbnail = location_attributes.jpeg_thumbnail
        return location_message

    def proto_to_location(self, proto):
        # type: (Message.LocationMessage) -> LocationAttributes
        return LocationAttributes(
            proto.degrees_latitude if proto.HasField("degrees_latitude") else None,
            proto.degrees_longitude if proto.HasField("degrees_longitude") else None,
            proto.name if proto.HasField("name") else None,
            proto.address if proto.HasField("address") else None,
            proto.url if proto.HasField("url") else None,
            proto.duration if proto.HasField("duration") else None,
            proto.accuracy_in_meters if proto.HasField("accuracy_in_meters") else None,
            proto.speed_in_mps if proto.HasField("speed_in_mps") else None,
            proto.degrees_clockwise_from_magnetic_north
            if proto.HasField("degrees_clockwise_from_magnetic_north") else None,
            proto.axolotl_sender_key_distribution_message
            if proto.HasField("axolotl_sender_key_distribution_message") else None,
            proto.jpeg_thumbnail if proto.HasField("jpeg_thumbnail") else None
        )

    def image_to_proto(self, image_attributes):
        # type: (ImageAttributes) -> Message.ImageMessage

        image_message = Message.ImageMessage()
        image_message.width = image_attributes.width
        image_message.height = image_attributes.height
        if image_attributes.caption is not None:
            image_message.caption = image_attributes.caption
        if image_attributes.jpeg_thumbnail is not None:
            image_message.jpeg_thumbnail = image_attributes.jpeg_thumbnail

        return self.downloadablemedia_to_proto(image_attributes.downloadablemedia_attributes, image_message)

    def proto_to_image(self, proto):
        # type: (Message.ImageMessage) -> ImageAttributes

        return ImageAttributes(
            self.proto_to_downloadablemedia(proto),
            proto.width, proto.height,
            proto.caption if proto.HasField("caption") else None,
            proto.jpeg_thumbnail if proto.HasField("jpeg_thumbnail") else None
        )

    def extendedtext_to_proto(self, extendedtext_attributes):
        # type: (ExtendedTextAttributes) -> Message.ExtendedTextMessage
        m = Message.ExtendedTextMessage()
        if extendedtext_attributes.text is not None:
            m.text = extendedtext_attributes.text
        if extendedtext_attributes.matched_text is not None:
            m.matched_text = extendedtext_attributes.matched_text
        if extendedtext_attributes.canonical_url is not None:
            m.canonical_url = extendedtext_attributes.canonical_url
        if extendedtext_attributes.description is not None:
            m.description = extendedtext_attributes.description
        if extendedtext_attributes.title is not None:
            m.title = extendedtext_attributes.title
        if extendedtext_attributes.jpeg_thumbnail is not None:
            m.jpeg_thumbnail = extendedtext_attributes.jpeg_thumbnail
        if extendedtext_attributes.context_info is not None:
            m.context_info.MergeFrom(self.contextinfo_to_proto(extendedtext_attributes.context_info))
        return m

    def proto_to_extendedtext(self, proto):
        # type: (Message.ExtendedTextMessage) -> ExtendedTextAttributes
        return ExtendedTextAttributes(
            proto.text if proto.HasField("text") else None,
            proto.matched_text if proto.HasField("matched_text") else None,
            proto.canonical_url if proto.HasField("canonical_url") else None,
            proto.description if proto.HasField("description") else None,
            proto.title if proto.HasField("title") else None,
            proto.jpeg_thumbnail if proto.HasField("jpeg_thumbnail") else None,
            self.proto_to_contextinfo(proto.context_info) if proto.HasField("context_info") else None
        )

    def document_to_proto(self, document_attributes):
        # type: (DocumentAttributes) -> Message.DocumentMessage

        m = Message.DocumentMessage()
        if document_attributes.file_name is not None:
            m.file_name = document_attributes.file_name
        if document_attributes.file_length is not None:
            m.file_length = document_attributes.file_length
        if document_attributes.title is not None:
            m.title = document_attributes.title
        if document_attributes.page_count is not None:
            m.page_count = document_attributes.page_count
        if document_attributes.jpeg_thumbnail is not None:
            m.jpeg_thumbnail = document_attributes.jpeg_thumbnail

        return self.downloadablemedia_to_proto(document_attributes.downloadablemedia_attributes, m)

    def proto_to_document(self, proto):
        return DocumentAttributes(
            self.downloadablemedia_to_proto(proto),
            proto.file_name if proto.HasField("file_name") else None,
            proto.file_length if proto.HasField("file_length") else None,
            proto.title if proto.HasField("title") else None,
            proto.page_count if proto.HasField("page_count") else None,
            proto.jpeg_thumbnail if proto.HasField("jpeg_thumbnail") else None
        )

    def downloadablemedia_to_proto(self, downloadablemedia_attributes, proto):
        # type: (DownloadableMediaMessageAttributes, object) -> object
        proto.mimetype = downloadablemedia_attributes.mimetype
        proto.file_length = downloadablemedia_attributes.file_length
        proto.file_sha256 = downloadablemedia_attributes.file_sha256
        proto.url = downloadablemedia_attributes.url
        proto.media_key = downloadablemedia_attributes.media_key

        return self.media_to_proto(downloadablemedia_attributes, proto)

    def proto_to_downloadablemedia(self, proto):
        return DownloadableMediaMessageAttributes(
            mimetype=proto.mimetype,
            file_length=proto.file_length,
            file_sha256=proto.file_sha256,
            url=proto.url,
            media_key=proto.media_key,
            context_info=self.proto_to_contextinfo(proto.context_info)
            if proto.HasField("context_info") else None
        )

    def media_to_proto(self, media_attributes, proto):
        # type: (MediaAttributes, object) -> object

        if media_attributes.context_info:
            proto.context_info.MergeFrom(self.contextinfo_to_proto(media_attributes.context_info))

        return proto

    def proto_to_media(self, proto):
        return MediaAttributes(
            context_info=proto.context_info if proto.HasField("context_info") else None
        )

    def contextinfo_to_proto(self, contextinfo_attributes):
        # type: (ContextInfoAttributes) -> ContextInfo
        cxt_info = ContextInfo()
        if contextinfo_attributes.stanza_id is not None:
            cxt_info.stanza_id = contextinfo_attributes.stanza_id
        if contextinfo_attributes.participant is not None:
            cxt_info.participant = contextinfo_attributes.participant
        if contextinfo_attributes.quoted_message:
            cxt_info.quoted_message.MergeFrom(self.message_to_proto(contextinfo_attributes.quoted_message))
        if contextinfo_attributes.remote_jid is not None:
            cxt_info.remote_jid = contextinfo_attributes.remote_jid
        if contextinfo_attributes.mentioned_jid is not None and len(contextinfo_attributes.mentioned_jid):
            cxt_info.mentioned_jid[:] = contextinfo_attributes.mentioned_jid
        if contextinfo_attributes.edit_version is not None:
            cxt_info.edit_version = contextinfo_attributes.edit_version
        if contextinfo_attributes.revoke_message is not None:
            cxt_info.revoke_message = contextinfo_attributes.revoke_message
        return cxt_info

    def proto_to_contextinfo(self, proto):
        # type: (ContextInfo) -> ContextInfoAttributes
        return ContextInfoAttributes(
            stanza_id=proto.stanza_id if proto.HasField("stanza_id") else None,
            participant=proto.participant if proto.HasField("participant") else None,
            quoted_message=self.proto_to_message(proto.quoted_message)
            if proto.HasField("quoted_message") else None,
            remote_jid=proto.remote_jid if proto.HasField("remote_jid") else None,
            mentioned_jid=proto.mentioned_jid if len(proto.mentioned_jid) else [],
            edit_version=proto.edit_version if proto.HasField("edit_version") else None,
            revoke_message=proto.revoke_message if proto.HasField("revoke_message") else None
        )

    def message_to_proto(self, message_attributes):
        # type: (MessageAttributes) -> Message
        message = Message()
        if message_attributes.conversation:
            message.conversation = message_attributes.conversation
        if message_attributes.image:
            message.image_message.MergeFrom(self.image_to_proto(message_attributes.image))
        if message_attributes.contact:
            message.contact_message.MergeFrom(self.contact_to_proto(message_attributes.contact))
        if message_attributes.location:
            message.location_message.MergeFrom(self.location_to_proto(message_attributes.location))
        if message_attributes.extended_text:
            message.extended_text_message.MergeFrom(self.extendedtext_to_proto(message_attributes.extended_text))
        if message_attributes.document:
            message.document_message.MergeFrom(self.document_to_proto(message_attributes.document))

        return message

    def proto_to_message(self, proto):
        # type: (Message) -> MessageAttributes
        conversation = proto.conversation if proto.conversation else None
        image = self.proto_to_image(proto.image_message) if proto.HasField("image_message") else None
        contact = self.proto_to_contact(proto.contact_message) if proto.HasField("contact_message") else None
        location = self.proto_to_location(proto.location_message) if proto.HasField("location_message") else None
        extended_text = self.proto_to_extendedtext(proto.extended_text_message) \
            if proto.HasField("extended_text_message") else None
        document = self.proto_to_document(proto.document_message) \
            if proto.HasField("document_message") else None
        audio = None
        video = None
        protocol = None

        return MessageAttributes(
            conversation,
            image,
            contact,
            location,
            extended_text,
            document,
            audio,
            video,
            protocol
        )

    def protobytes_to_message(self, protobytes):
        # type: (bytes) -> MessageAttributes
        m = Message()
        m.ParseFromString(protobytes)
        return self.proto_to_message(m)

    def message_to_protobytes(self, message):
        # type: (MessageAttributes) -> bytes
        return self.message_to_proto(message).SerializeToString()
