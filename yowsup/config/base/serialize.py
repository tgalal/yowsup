class ConfigSerialize(object):

    def __init__(self, transforms):
        self._transforms = transforms

    def serialize(self, config):
        """
        :param config:
        :type config: yowsup.config.base.config.Config
        :return:
        :rtype: bytes
        """
        for transform in self._transforms:
            config = transform.transform(config)
        return config

    def deserialize(self, data):
        """
        :type cls: type
        :param data:
        :type data: bytes
        :return:
        :rtype: yowsup.config.base.config.Config
        """
        for transform in self._transforms[::-1]:
            data = transform.reverse(data)
        return data
