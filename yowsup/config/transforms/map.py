from yowsup.config.base.transform import ConfigTransform


class MapTransform(ConfigTransform):

    def __init__(self, transform_map=None, reverse_map=None):
        """
        :param transform_map:
        :type transform_map: function | None
        :param reverse_map:
        :type reverse_map: function | None
        """
        self._transform_map = transform_map  # type: function | None
        self._reverse_map = reverse_map  # type: function | None

    def transform(self, data):
        if self._transform_map is not None:
            out = {}
            for key, val in data.items():
                key, val = self._transform_map(key, val)
                out[key] = val
            return out
        return data

    def reverse(self, data):
        if self._reverse_map is not None:
            out = {}
            for key, val in data.items():
                key, val = self._reverse_map(key, val)
                out[key] = val
            return out
        return data
