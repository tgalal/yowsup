from yowsup.config.base.transform import ConfigTransform
import json


class DictJsonTransform(ConfigTransform):
    def transform(self, data):
        return json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    def reverse(self, data):
        return json.loads(data)

