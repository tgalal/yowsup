class NoSessionException(Exception):
    pass


class UntrustedIdentityException(Exception):
    def __init__(self, name, identity_key):
        self._name = name
        self._identity_key = identity_key

    @property
    def name(self):
        return self._name

    @property
    def identity_key(self):
        return self._identity_key


class InvalidMessageException(Exception):
    pass


class InvalidKeyIdException(Exception):
    pass


class DuplicateMessageException(Exception):
    pass

