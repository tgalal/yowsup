from yowsup.config.base.transform import ConfigTransform
import types


class PropsTransform(ConfigTransform):
    def __init__(self, transform_map=None, reverse_map=None):
        self._transform_map = transform_map or {}
        self._reverse_map = reverse_map or {}

    def transform(self, data):
        """
        :param data:
        :type data: dict
        :return:
        :rtype: dict
        """
        out = {}
        for key, val in data.items():
            if key in self._transform_map:
                target = self._transform_map[key]
                key, val = target(key, val) if type(target) == types.FunctionType else (key, target)

            out[key] = val


        return out

    def reverse(self, data):
        transformed_dict = {}

        for key, val in data.items():
            if key in self._reverse_map:
                target = self._reverse_map[key]
                key, val = target(key, val) if type(target) == types.FunctionType else (key, target)

            transformed_dict[key] = val

        return transformed_dict
