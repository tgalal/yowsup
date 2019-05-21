class LocationAttributes(object):
    def __init__(self,
                 degrees_latitude, degrees_longitude,
                 name=None, address=None, url=None,
                 duration=None, accuracy_in_meters=None, speed_in_mps=None, degrees_clockwise_from_magnetic_north=None,
                 axolotl_sender_key_distribution_message=None, jpeg_thumbnail=None):
        """
        :param degrees_latitude: Actual location, Place
        :param degrees_longitude:  Actual location, Place
        :param name: Place
        :param address: Place
        :param url: Place
        :param duration:
        :param accuracy_in_meters:
        :param speed_in_mps:
        :param degrees_clockwise_from_magnetic_north:
        :param axolotl_sender_key_distribution_message:
        :param jpeg_thumbnail: Actual location, Place
        """

        self._degrees_latitude = degrees_latitude
        self._degrees_longitude = degrees_longitude
        self._name = name
        self._address = address
        self._url = url
        self._duration = duration
        self._accuracy_in_meters = accuracy_in_meters
        self._speed_in_mps = speed_in_mps
        self._degrees_clockwise_from_magnetic_north = degrees_clockwise_from_magnetic_north
        self._axolotl_sender_key_distribution_message = axolotl_sender_key_distribution_message
        self._jpeg_thumbnail = jpeg_thumbnail

    def __str__(self):
        attrs = []
        if self.degrees_latitude is not None:
            attrs.append(("degrees_latitude", self.degrees_latitude))
        if self.degrees_longitude is not None:
            attrs.append(("degrees_longitude", self.degrees_longitude))
        if self.name is not None:
            attrs.append(("name", self.name))
        if self.address is not None:
            attrs.append(("address", self.address))
        if self.url is not None:
            attrs.append(("url", self.url))
        if self.duration is not None:
            attrs.append(("duration", self.duration))
        if self.accuracy_in_meters is not None:
            attrs.append(("accuracy_in_meters", self.accuracy_in_meters))
        if self.speed_in_mps is not None:
            attrs.append(("speed_in_mps", self.speed_in_mps))
        if self.degrees_clockwise_from_magnetic_north is not None:
            attrs.append(("degrees_clockwise_from_magnetic_north", self.degrees_clockwise_from_magnetic_north))
        if self.axolotl_sender_key_distribution_message is not None:
            attrs.append(("axolotl_sender_key_distribution_message", "[binary data]"))
        if self.jpeg_thumbnail is not None:
            attrs.append(("jpeg_thumbnail", "[binary data]"))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def degrees_latitude(self):
        return self._degrees_latitude

    @degrees_latitude.setter
    def degrees_latitude(self, value):
        self._degrees_latitude = value

    @property
    def degrees_longitude(self):
        return self._degrees_longitude

    @degrees_longitude.setter
    def degrees_longitude(self, value):
        self._degrees_longitude = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        self._address = value

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, value):
        self._url = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = value

    @property
    def accuracy_in_meters(self):
        return self._accuracy_in_meters

    @accuracy_in_meters.setter
    def accuracy_in_meters(self, value):
        self._accuracy_in_meters = value

    @property
    def speed_in_mps(self):
        return self._speed_in_mps

    @speed_in_mps.setter
    def speed_in_mps(self, value):
        self._speed_in_mps = value

    @property
    def degrees_clockwise_from_magnetic_north(self):
        return self._degrees_clockwise_from_magnetic_north

    @degrees_clockwise_from_magnetic_north.setter
    def degrees_clockwise_from_magnetic_north(self, value):
        self._degrees_clockwise_from_magnetic_north = value

    @property
    def axolotl_sender_key_distribution_message(self):
        return self._axolotl_sender_key_distribution_message

    @axolotl_sender_key_distribution_message.setter
    def axolotl_sender_key_distribution_message(self, value):
        self._axolotl_sender_key_distribution_message = value

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail

    @jpeg_thumbnail.setter
    def jpeg_thumbnail(self, value):
        self._jpeg_thumbnail = value
