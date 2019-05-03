class ContactAttributes(object):
    def __init__(self, display_name, vcard):
        self._display_name = display_name
        self._vcard = vcard

    @property
    def display_name(self):
        return self._display_name

    @property
    def vcard(self):
        return self._vcard
