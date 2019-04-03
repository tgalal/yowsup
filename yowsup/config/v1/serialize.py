from yowsup.config.base import serialize
from yowsup.config.transforms.filter import FilterTransform
from yowsup.config.transforms.meta import MetaPropsTransform
from yowsup.config.transforms.map import MapTransform
from yowsup.config.transforms.config_dict import ConfigDictTransform


class ConfigSerialize(serialize.ConfigSerialize):
    def __init__(self, config_class):
        super(ConfigSerialize, self).__init__(
            transforms=(
                ConfigDictTransform(config_class),
                FilterTransform(
                    transform_filter=lambda key, val: val is not None,
                    reverse_filter=lambda key, val: key != "version"
                ),
                MapTransform(transform_map=lambda key, val: (key[1:], val)),
                MetaPropsTransform(meta_props=("version", )),
            )
        )
