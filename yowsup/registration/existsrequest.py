from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.env import YowsupEnv


class WAExistsRequest(WARequest):

    def __init__(self, config):
        """
        :param config:
        :type config: yowsup.config.v1.config.Config
        """
        super(WAExistsRequest,self).__init__(config)
        if config.id is None:
            raise ValueError("Config does not contain id")

        self.url = "v.whatsapp.net/v2/exist"

        self.pvars = ["status", "reason", "sms_length", "voice_length", "result","param", "login", "type",
                      "chat_dns_domain", "edge_routing_info"
                    ]

        self.setParser(JSONResponseParser())
        self.addParam("token", YowsupEnv.getCurrent().getToken(self._p_in))
