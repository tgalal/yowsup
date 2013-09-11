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

from Yowsup.Common.Http.warequest import WARequest
from Yowsup.Common.Http.waresponseparser import JSONResponseParser
from Yowsup.Common.constants import Constants
from Yowsup.Common.utilities import Utilities
import os
class WACodeRequest(WARequest):

	def __init__(self,cc, p_in, idx, method="sms"):
		super(WACodeRequest,self).__init__();

		self.p_in = p_in #number

		self.addParam("cc", cc);
		self.addParam("in", p_in);
		self.addParam("lc", "US");
		self.addParam("lg", "en");
		self.addParam("mcc", "000");
		self.addParam("mnc", "000");
		self.addParam("method", method);
		self.addParam("id", idx)

		self.currentToken = Utilities.readToken()

		if self.currentToken:
			print("Read token from %s " % os.path.expanduser(Constants.tokenStorage))
		else:
			self.currentToken = Constants.tokenData

		self.addParam("token", self.getToken(p_in, self.currentToken["t"]))

		self.url = "v.whatsapp.net/v2/code"

		self.pvars = ["status","reason","length", "method", "retry_after", "code", "param"] +\
					["login", "pw", "type", "expiration", "kind", "price", "cost", "currency", "price_expiration"]

		self.setParser(JSONResponseParser())

	def send(self, parser = None):
		res = super(WACodeRequest, self).send(parser)

		#attempt recovery by fetching new token
		if res:
			if res["status"] == "fail":
				if res["reason"] in ("old_version", "bad_token") and Utilities.tokenCacheEnabled:

					print("Failed, reason: %s. Checking for a new token.." % res["reason"])

					res = WARequest.sendRequest(Constants.tokenSource[0], 80, Constants.tokenSource[1], {}, {})

					if res:
						tokenData = res.read()
						pvars = ["v", "r", "u", "t", "d"]
						jParser = JSONResponseParser()
						parsed = jParser.parse(tokenData.decode(), pvars)

						if(
									parsed["v"] != self.currentToken["v"]
							or 	parsed["r"] != self.currentToken["r"]
							or 	parsed["u"] != self.currentToken["u"]
							or 	parsed["t"] != self.currentToken["t"]
							or 	parsed["d"] != self.currentToken["d"]
						):
							self.currentToken = parsed
							print("Fetched a new token, persisting !")

							self.removeParam("token")

							print("Now retrying the request..")
							self.addParam("token", self.getToken(self.p_in, self.currentToken["t"]))
						else:
							print("No new tokens :(")

						res = super(WACodeRequest, self).send(parser)

						if res and res["status"] != "fail":
							Utilities.persistToken(tokenData) #good token

		return res	

