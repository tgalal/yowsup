from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_key import MessageKeyAttributes


class ProtocolAttributes(object):
    TYPE_REOVOKE = 0
    TYPES = {
        TYPE_REOVOKE: "REVOKE"
    }

    def __init__(self, key, type):
        self.key = key
        self.type = type

    def __str__(self):
        return "[type=%s, key=%s]" % (self.TYPES[self.type], self.key)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        assert isinstance(value, MessageKeyAttributes), type(value)
        self._key = value

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        assert value in self.TYPES, "Unknown type: %s" % value
        self._type = value
