from yowsup.config.base import config
import logging

logger = logging.getLogger(__name__)


class Config(config.Config):
    def __init__(
            self,
            phone=None,
            cc=None,
            password=None,
            pushname=None,
            id=None,
            mcc=None,
            mnc=None,
            sim_mcc=None,
            sim_mnc=None,
            client_static_keypair=None,
            server_static_public=None,
            expid=None,
            fdid=None,
            edge_routing_info=None,
            chat_dns_domain=None
    ):
        super(Config, self).__init__(1)

        self._phone = str(phone) if phone is not None else None  # type: str
        self._cc = cc  # type: int
        self._password = password  # type: str
        self._pushname = pushname  # type: str
        self._id = id
        self._client_static_keypair = client_static_keypair
        self._server_static_public = server_static_public
        self._expid = expid
        self._fdid = fdid
        self._mcc = mcc
        self._mnc = mnc
        self._sim_mcc = sim_mcc
        self._sim_mnc = sim_mnc
        self._edge_routing_info = edge_routing_info
        self._chat_dns_domain = chat_dns_domain

        if self._password is not None:
            logger.warn("Setting a password in Config is deprecated and not used anymore. "
                        "client_static_keypair is used instead")

    def __str__(self):
        from yowsup.config.v1.serialize import ConfigSerialize
        from yowsup.config.transforms.dict_json import DictJsonTransform
        return DictJsonTransform().transform(ConfigSerialize(self.__class__).serialize(self))

    @property
    def phone(self):
        return self._phone

    @phone.setter
    def phone(self, value):
        self._phone = str(value) if value is not None else None

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
        if value is not None:
            logger.warn("Setting a password in Config is deprecated and not used anymore. "
                        "client_static_keypair is used instead")

    @property
    def pushname(self):
        return self._pushname

    @pushname.setter
    def pushname(self, value):
        self._pushname = value

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

    @id.setter
    def id(self, value):
        self._id = value

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
    def expid(self):
        return self._expid

    @expid.setter
    def expid(self, value):
        self._expid = value

    @property
    def fdid(self):
        return self._fdid

    @fdid.setter
    def fdid(self, value):
        self._fdid = value

    @property
    def edge_routing_info(self):
        return self._edge_routing_info

    @edge_routing_info.setter
    def edge_routing_info(self, value):
        self._edge_routing_info = value

    @property
    def chat_dns_domain(self):
        return self._chat_dns_domain

    @chat_dns_domain.setter
    def chat_dns_domain(self, value):
        self._chat_dns_domain = value
