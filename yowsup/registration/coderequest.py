from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.common.tools import WATools
from yowsup.registration.existsrequest import WAExistsRequest
from yowsup.env import YowsupEnv


class WACodeRequest(WARequest):
    def __init__(self, method, config):
        """
        :type method: str
        :param config:
        :type config: yowsup.config.v1.config.Config
        """
        super(WACodeRequest,self).__init__(config)

        self.addParam("mcc", config.mcc.zfill(3))
        self.addParam("mnc", config.mnc.zfill(3))
        self.addParam("sim_mcc", config.sim_mcc.zfill(3))
        self.addParam("sim_mnc", config.sim_mnc.zfill(3))
        self.addParam("method", method)
        self.addParam("reason", "")
        self.addParam("token", YowsupEnv.getCurrent().getToken(self._p_in))
        self.addParam("hasav", "1")

        self.url = "v.whatsapp.net/v2/code"

        self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
                    ["login", "type", "sms_wait", "voice_wait"]
        self.setParser(JSONResponseParser())

    def send(self, parser = None, encrypt=True, preview=False):
        if self. _config.id is not None:
            request = WAExistsRequest(self._config)
            result = request.send(encrypt=encrypt, preview=preview)

            if result:
                if result["status"] == "ok":
                    return result
                elif result["status"] == "fail" and "reason" in result and result["reason"] == "blocked":
                    return result
        else:
            self._config.id = WATools.generateIdentity()
            self.addParam("id", self._config.id)

        res = super(WACodeRequest, self).send(parser, encrypt=encrypt, preview=preview)

        return res
