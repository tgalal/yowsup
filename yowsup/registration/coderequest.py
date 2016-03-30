from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
# from yowsup.env import CURRENT_ENV
from yowsup.common.tools import StorageTools, WATools
from yowsup.registration.existsrequest import WAExistsRequest
from yowsup.env import S40YowsupEnv, AndroidYowsupEnv
import random, hashlib, os
CURRENT_ENV = AndroidYowsupEnv()

class WACodeRequest(WARequest):

    def __init__(self,cc, p_in, mcc= "000", mnc = "000", sim_mcc = "000", sim_mnc = "000", method="sms"):
        super(WACodeRequest,self).__init__()
        idx = StorageTools.getIdentity(cc + p_in)

        self.p_in = p_in
        self.__id = idx
        self.cc = cc

        self.addParam("cc", cc)
        self.addParam("in", p_in)
        self.addParam("lc", "GB")
        self.addParam("lg", "en")
        self.addParam("sim_mcc", sim_mcc.zfill(3))
        self.addParam("sim_mnc", sim_mnc.zfill(3))
        self.addParam("mcc", sim_mcc.zfill(3))
        self.addParam("mnc", sim_mnc.zfill(3))
        self.addParam("method", method)

        self.addParam("mistyped", "6")
        self.addParam("network_radio_type", "1")
        self.addParam("simnum", "1")
        self.addParam("s", "")
        self.addParam("copiedrc", "1")
        self.addParam("hasinrc", "1")
        self.addParam("rcmatch", "1")
        self.addParam("pid", os.getpid())
        self.addParam("rchash", hashlib.sha256(os.urandom(20)).hexdigest())
        self.addParam("anhash", hashlib.md5(os.urandom(20)).hexdigest())
        self.addParam("extexist", "1")
        self.addParam("extstate", "1")

        self.addParam("token", CURRENT_ENV.getToken(p_in))

        self.url = "v.whatsapp.net/v2/code"

        self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
                    ["login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration"]

        self.setParser(JSONResponseParser())

    def send(self, parser = None):
        if self.__id is not None:
            request = WAExistsRequest(self.cc, self.p_in, self.__id)
            result = request.send()
            if result["status"] == "ok":
                return result

        self.__id = WATools.generateIdentity()
        self.addParam("id", self.__id)

        res = super(WACodeRequest, self).send(parser)
        if res["status"] == "sent":
            StorageTools.writeIdentity(self.cc + self.p_in, self.__id)
        return res
