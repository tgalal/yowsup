from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser

class WAExistsRequest(WARequest):
    
    def __init__(self,cc, p_in, idx):
        super(WAExistsRequest,self).__init__();

        self.addParam("cc", cc);
        self.addParam("in", p_in);
        self.addParam("id", idx);

        self.url = "v.whatsapp.net/v2/exist"

        self.pvars = ["status", "reason", "sms_length", "voice_length", "result","param", "pw", "login", "type", "expiration", "kind",
                    "price", "cost", "currency", "price_expiration"
                    ]

        self.setParser(JSONResponseParser())