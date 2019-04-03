from yowsup.config.base.transform import ConfigTransform


class FilterTransform(ConfigTransform):

    def __init__(self, transform_filter=None, reverse_filter=None):
        """
        :param transform_filter:
        :type transform_filter: function | None
        :param reverse_filter:
        :type reverse_filter: function | None
        """
        self._transform_filter = transform_filter  # type: function | None
        self._reverse_filter = reverse_filter  # type: function | None

    def transform(self, data):
        if self._transform_filter is not None:
            out = {}
            for key, val in data.items():
                if self._transform_filter(key, val):
                    out[key] = val
            return out
        return data

    def reverse(self, data):
        if self._reverse_filter is not None:
            out = {}
            for key, val in data.items():
                if self._reverse_filter(key, val):
                    out[key] = val
            return out
        return data
