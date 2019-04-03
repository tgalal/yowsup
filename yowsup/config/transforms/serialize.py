from yowsup.config.transforms.props import PropsTransform


class SerializeTransform(PropsTransform):

    def __init__(self, serialize_map):
        """
        {
            "keystore": serializer
        }
        :param serialize_map:
        :type serialize_map:
        """
        transform_map = {}
        reverse_map = {}
        for key, val in serialize_map:
            transform_map[key] = lambda key, val: key, serialize_map[key].serialize(val)
            reverse_map[key] = lambda key, val: key, serialize_map[key].deserialize(val)

        super(SerializeTransform, self).__init__(transform_map=transform_map, reverse_map=reverse_map)

