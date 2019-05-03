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

    @property
    def degrees_latitude(self):
        return self._degrees_latitude

    @property
    def degrees_longitude(self):
        return self._degrees_longitude

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def url(self):
        return self._url

    @property
    def duration(self):
        return self._duration

    @property
    def accuracy_in_meters(self):
        return self._accuracy_in_meters

    @property
    def speed_in_mps(self):
        return self._speed_in_mps

    @property
    def degrees_clockwise_from_magnetic_north(self):
        return self._degrees_clockwise_from_magnetic_north

    @property
    def axolotl_sender_key_distribution_message(self):
        return self._axolotl_sender_key_distribution_message

    @property
    def jpeg_thumbnail(self):
        return self._jpeg_thumbnail
