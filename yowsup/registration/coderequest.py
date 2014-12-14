from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.common import YowConstants as Constants
import os


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

        self.currentToken = None#Utilities.readToken()

        if self.currentToken:
            print("Read token from %s " % os.path.expanduser(Constants.tokenStorage))
        else:
            self.currentToken = Constants.DATA_CLIENT

        self.addParam("token", self.getToken(p_in, self.currentToken["t"]))

        self.url = "v.whatsapp.net/v2/code"

        self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
                    ["login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration"]

        self.setParser(JSONResponseParser())

    def send(self, parser = None):
        res = super(WACodeRequest, self).send(parser)
        return res
        #attempt recovery by fetching new token
        # if res:
        #     if res["status"] == "fail":
        #         if res["reason"] in ("old_version", "bad_token") and Utilities.tokenCacheEnabled:

        #             print("Failed, reason: %s. Checking for a new token.." % res["reason"])

        #             res = WARequest.sendRequest(Constants.tokenSource[0], 80, Constants.tokenSource[1], {}, {})

        #             if res:
        #                 tokenData = res.read()
        #                 pvars = ["v", "r", "u", "t", "d"]
        #                 jParser = JSONResponseParser()
        #                 parsed = jParser.parse(tokenData.decode(), pvars)

        #                 if(
        #                             parsed["v"] != self.currentToken["v"]
        #                     or  parsed["r"] != self.currentToken["r"]
        #                     or  parsed["u"] != self.currentToken["u"]
        #                     or  parsed["t"] != self.currentToken["t"]
        #                     or  parsed["d"] != self.currentToken["d"]
        #                 ):
        #                     self.currentToken = parsed
        #                     print("Fetched a new token, persisting !")

        #                     self.removeParam("token")

        #                     print("Now retrying the request..")
        #                     self.addParam("token", self.getToken(self.p_in, self.currentToken["t"]))
        #                 else:
        #                     print("No new tokens :(")

        #                 res = super(WACodeRequest, self).send(parser)

        #                 if res and res["status"] != "fail":
        #                     Utilities.persistToken(tokenData) #good token

        # return res  

