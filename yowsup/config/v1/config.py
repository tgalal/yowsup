from yowsup.config.base import config


class Config(config.Config):

    def __init__(self,
                 phone=None,
                 cc=None,
                 password=None,
                 id=None,
                 mcc=None,
                 mnc=None,
                 sim_mcc=None,
                 sim_mnc=None
                 ):
        super(Config, self).__init__(1)

        self._phone = str(phone) # type: str
        self._cc = cc  # type: int
        self._password = password  # type: str
        self._id = id
        self._mcc = mcc
        self._mnc = mnc
        self._sim_mcc = sim_mcc
        self._sim_mnc = sim_mnc

    def __str__(self):
        from yowsup.config.v1.serialize import ConfigSerialize
        from yowsup.config.transforms.dict_json import DictJsonTransform
        return DictJsonTransform().transform(ConfigSerialize(self.__class__).serialize(self))

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = value

    @property
    def cc(self):
        return self._cc

    @cc.setter
    def cc(self, value):
        self._cc = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    @property
    def mcc(self):
        return self._mcc

    @mcc.setter
    def mcc(self, value):
        self._mcc = value

    @property
    def mnc(self):
        return self._mnc

    @mnc.setter
    def mnc(self, value):
        self._mnc = value

    @property
    def sim_mcc(self):
        return self._sim_mcc

    @sim_mcc.setter
    def sim_mcc(self, value):
        self._sim_mcc = value

    @property
    def sim_mnc(self):
        return self._sim_mnc

    @sim_mnc.setter
    def sim_mnc(self, value):
        self._sim_mnc = value

    @property
    def id(self):
        return self._id
