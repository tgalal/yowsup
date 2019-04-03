class Config(object):
    def __init__(self, version):
        self._version = version

    def __contains__(self, item):
        return self[item] is not None

    def __getitem__(self, item):
        return getattr(self, "_%s" % item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    @property
    def version(self):
        return self._version
