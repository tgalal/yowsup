'''
Copyright (c) <2012> Tarek Galal <tare2.galal@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this
software and associated documentation files (the "Software"), to deal in the Software
without restriction, including without limitation the rights to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR
A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

from yowsup.common.http.warequest import WARequest
from yowsup.common.http.waresponseparser import JSONResponseParser
from yowsup.common.tools import StorageTools
import hashlib
import os

class WARegRequest(WARequest):

    def __init__(self,cc, p_in, code):
        super(WARegRequest,self).__init__()
        idx = StorageTools.getIdentity(cc + p_in)

        if idx is None:
            raise ValueError("You have to request code first")

        self.addParam("cc", cc)
        self.addParam("in", p_in)

        self.addParam("id", idx)
        self.addParam("code", code)

        self.addParam("lc", "GB")
        self.addParam("lg", "en")

        self.addParam("mistyped", '6')
        # self.addParam('network_radio_type', '1')
        self.addParam('simnum', '1')
        self.addParam('s', '')
        self.addParam('copiedrc', '1')
        self.addParam('hasinrc', '1')
        self.addParam('rcmatch', '1')
        self.addParam('pid', os.getpid())
        self.addParam('rchash', hashlib.sha256(os.urandom(20)).hexdigest())
        self.addParam('anhash', hashlib.md5(os.urandom(20)).hexdigest())
        self.addParam('extexist', '1')
        self.addParam('extstate', '1')

        self.url = "v.whatsapp.net/v2/register"

        self.pvars = ["status", "login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration",
                      "reason","retry_after"]

        self.setParser(JSONResponseParser())

    def register(self):
        return self.send()
