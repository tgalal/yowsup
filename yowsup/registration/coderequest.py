from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.common.tools import StorageTools, WATools
from yowsup.registration.existsrequest import WAExistsRequest
from yowsup.env import YowsupEnv
import random, hashlib, os


class WACodeRequest(WARequest):
    def __init__(self, method, config):
        """
        :type method: str
        :param config:
        :type config: yowsup.config.vx.config.Config
        """
        super(WACodeRequest,self).__init__()
        self._config = config
        idx = StorageTools.getIdentity(config.phone)

        self._p_in = str(config.phone)[len(str(config.cc)):]
        self.__id = idx

        self.addParam("cc", config.cc)
        self.addParam("in", self._p_in)
        self.addParam("lc", "GB")
        self.addParam("lg", "en")
        self.addParam("sim_mcc", config.sim_mcc.zfill(3))
        self.addParam("sim_mnc", config.sim_mnc.zfill(3))
        self.addParam("mcc", config.mcc.zfill(3))
        self.addParam("mnc", config.mnc.zfill(3))
        self.addParam("method", method)

        self.addParam("mistyped", "6")
        self.addParam("network_radio_type", "1")
        self.addParam("simnum", "1")
        self.addParam("s", "")
        self.addParam("copiedrc", "1")
        self.addParam("hasinrc", "1")
        self.addParam("rcmatch", "1")
        self.addParam("pid", int(random.uniform(100,9999)))
        self.addParam("rchash", hashlib.sha256(os.urandom(20)).hexdigest())
        self.addParam("anhash", os.urandom(20))
        self.addParam("extexist", "1")
        self.addParam("extstate", "1")

        self.addParam("token", YowsupEnv.getCurrent().getToken(self._p_in))

        self.url = "v.whatsapp.net/v2/code"

        self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
                    ["login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration"]

        self.setParser(JSONResponseParser())

    def send(self, parser = None):
        if self.__id is not None:
            request = WAExistsRequest(self._config, self.__id)
            result = request.send()
            if result["status"] == "ok":
                return result
            elif result["status"] == "fail" and "reason" in result and result["reason"] == "blocked":
                return result

        self.__id = WATools.generateIdentity()
        self.addParam("id", self.__id)

        res = super(WACodeRequest, self).send(parser)
        if res["status"] == "sent":
            StorageTools.writeIdentity(self._config.cc + self._p_in, self.__id)
        return res
