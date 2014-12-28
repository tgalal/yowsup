from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.env import CURRENT_ENV

class WACodeRequest(WARequest):

    def __init__(self,cc, p_in, idx, mcc= "000", mnc = "000", sim_mcc = "000", sim_mnc = "000", method="sms"):
        super(WACodeRequest,self).__init__()

        self.p_in = p_in

        self.addParam("cc", cc)
        self.addParam("in", p_in)
        self.addParam("lc", "US")
        self.addParam("lg", "en")
        self.addParam("mcc", "000")
        self.addParam("mnc", "000")
        self.addParam("sim_mcc", sim_mcc.zfill(3))
        self.addParam("sim_mnc", sim_mnc.zfill(3))
        self.addParam("method", method)
        self.addParam("id", idx)
        self.addParam("network_radio_type", "1")
        self.addParam("reason", "self-send-jailbroken")


        self.addParam("token", CURRENT_ENV.getToken(p_in))

        self.url = "v.whatsapp.net/v2/code"

        self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
                    ["login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration"]

        self.setParser(JSONResponseParser())

    def send(self, parser = None):
        res = super(WACodeRequest, self).send(parser)
        return res

