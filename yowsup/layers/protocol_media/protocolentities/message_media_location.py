from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes
from .message_media import MediaMessageProtocolEntity
from .attributes.attributes_location import LocationAttributes
from .attributes.attributes_media import MediaAttributes


class LocationMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    def __init__(self, location_attrs, media_message_attrs, message_attrs):
        # type: (LocationAttributes, MediaAttributes, MessageAttributes) -> None
        super(LocationMediaMessageProtocolEntity, self).__init__("location", media_message_attrs, message_attrs)
        self.degrees_latitude = location_attrs.degrees_latitude
        self.degrees_longitude = location_attrs.degrees_longitude
        self.name = location_attrs.name
        self.address = location_attrs.address
        self.url = location_attrs.url
        self.duration = location_attrs.duration
        self.accuracy_in_meters = location_attrs.accuracy_in_meters
        self.speed_in_mps = location_attrs.speed_in_mps
        self.degrees_clockwise_from_magnetic_north = location_attrs.degrees_clockwise_from_magnetic_north
        self.axolotl_sender_key_distribution_message = location_attrs.axolotl_sender_key_distribution_message
        self.jpeg_thumbnail = location_attrs.jpeg_thumbnail

    @property
    def proto(self):
        return self._proto.location_message

    @property
    def degrees_latitude(self):
        return self.proto.degrees_latitude

    @degrees_latitude.setter
    def degrees_latitude(self, value):
        self.proto.degrees_latitude = value

    @property
    def degrees_longitude(self):
        return self.proto.degrees_longitude

    @degrees_longitude.setter
    def degrees_longitude(self, value):
        self.proto.degrees_longitude = value

    @property
    def name(self):
        return self.proto.name

    @name.setter
    def name(self, value):
        self.proto.name = value

    @property
    def address(self):
        return self.proto.addrees

    @address.setter
    def address(self, value):
        self.proto.address = value

    @property
    def url(self):
        return self.proto.url

    @url.setter
    def url(self, value):
        self.proto.url = value

    @property
    def duration(self):
        return self.proto.duration

    @duration.setter
    def duration(self, value):
        self.proto.duration = value

    @property
    def accuracy_in_meters(self):
        return self.proto.accuracy_in_meters

    @accuracy_in_meters.setter
    def accuracy_in_meters(self, value):
        self.proto.accuracy_in_meters = value

    @property
    def speed_in_mps(self):
        return self.proto.speed_in_mps

    @speed_in_mps.setter
    def speed_in_mps(self, value):
        self.proto.speed_in_mps = value

    @property
    def degrees_clockwise_from_magnetic_north(self):
        return self.proto.degrees_clockwise_from_magnetic_north

    @degrees_clockwise_from_magnetic_north.setter
    def degrees_clockwise_from_magnetic_north(self, value):
        self.proto.degrees_clockwise_from_magnetic_north = value

    @property
    def axolotl_sender_key_distribution_message(self):
        return self.proto.axolotl_sender_key_distribution_message

    @axolotl_sender_key_distribution_message.setter
    def axolotl_sender_key_distribution_message(self, value):
        self.proto.axolotl_sender_key_distribution_message = value

    @property
    def jpeg_thumbnail(self):
        return self.proto.jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self.proto.jpeg_thumbnail = value
