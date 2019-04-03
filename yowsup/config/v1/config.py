from yowsup.config.base import config


class Config(config.Config):

    def __init__(
            self,
            phone=None,
            cc=None,
            password=None,
            id=None,
            mcc=None,
            mnc=None,
            sim_mcc=None,
            sim_mnc=None,
            client_static_keypair=None,
            server_static_public=None,
            device_id=None
    ):
        super(Config, self).__init__(1)

        self._phone = str(phone)  # type: str
        self._cc = cc  # type: int
        self._password = password  # type: str
        self._id = id
        self._client_static_keypair = client_static_keypair
        self._server_static_public = server_static_public
        self._device_id = device_id
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

    @property
    def client_static_keypair(self):
        return self._client_static_keypair

    @client_static_keypair.setter
    def client_static_keypair(self, value):
        self._client_static_keypair = value

    @property
    def server_static_public(self):
        return self._server_static_public

    @server_static_public.setter
    def server_static_public(self, value):
        self._server_static_public = value

    @property
    def device_id(self):
        return self._device_id

    @device_id.setter
    def device_id(self, value):
        self._device_id = value
