from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.env import CURRENT_ENV
import os

class WAExistsRequest(WARequest):

    def __init__(self,cc, p_in, idx):
        super(WAExistsRequest,self).__init__()

        self.addParam("cc", cc)
        self.addParam("in", p_in)
        self.addParam("id", idx)
        self.addParam("lg", "en")
        self.addParam("lc", "GB")
        self.addParam("token", CURRENT_ENV.getToken(p_in))
        self.addParam("mistyped", '6')
        self.addParam('network_radio_type', '1')
        self.addParam('simnum', '1')
        self.addParam('s', '')
        self.addParam('copiedrc', '1')
        self.addParam('hasinrc', '1')
        self.addParam('rcmatch', '1')
        self.addParam('pid', os.getpid())
        self.addParam('extexist', '1')
        self.addParam('extstate', '1')

        self.url = "v.whatsapp.net/v2/exist"

        self.pvars = ["status", "reason", "sms_length", "voice_length", "result","param", "pw", "login", "type", "expiration", "kind",
                    "price", "cost", "currency", "price_expiration"
                    ]

        self.setParser(JSONResponseParser())

    def send(self, parser = None):
        res = super(WAExistsRequest, self).send(parser)
        return res
