from yowsup.config.base.transform import ConfigTransform


class DictKeyValTransform(ConfigTransform):
    def transform(self, data):
        """
        :param data:
        :type data: dict
        :return:
        :rtype:
        """
        out=[]
        keys = sorted(data.keys())
        for k in keys:
            out.append("%s=%s" % (k, data[k]))
        return "\n".join(out)

    def reverse(self, data):
        out = {}
        for l in data.split('\n'):
            line = l.strip()
            if len(line) and line[0] not in ('#',';'):
                prep = line.split('#', 1)[0].split(';', 1)[0].split('=', 1)
                varname = prep[0].strip()
                val = prep[1].strip()
                out[varname.replace('-', '_')] = val
        return out
