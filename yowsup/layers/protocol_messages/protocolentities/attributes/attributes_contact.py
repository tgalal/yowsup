class ContactAttributes(object):
    def __init__(self, display_name, vcard, context_info=None):
        self._display_name = display_name
        self._vcard = vcard
        self._context_info = context_info

    def __str__(self):
        attrs = []
        if self.display_name is not None:
            attrs.append(("display_name", self.display_name))
        if self.vcard is not None:
            attrs.append(("vcard", "[binary data]"))
        if self.context_info is not None:
            attrs.append(("context_info", self.context_info))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def display_name(self):
        return self._display_name

    @display_name.setter
    def display_name(self, value):
        self._display_name = value

    @property
    def vcard(self):
        return self._vcard

    @vcard.setter
    def vcard(self, value):
        self._vcard = value

    @property
    def context_info(self):
        return self._context_info

    @context_info.setter
    def context_info(self, value):
        self.context_info = value
