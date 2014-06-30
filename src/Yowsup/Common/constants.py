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

class Constants:
	host = "c2.whatsapp.net"
	port = 443
	domain = "s.whatsapp.net"

	v="0.90"

	tokenData = {
		"v": "2.12.15",
		"r": "S40-2.12.15",
		"u": "WhatsApp/2.12.15 S40Version/14.26 Device/Nokia302",
		"t": "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1391039105258{phone}",
		"d": "Nokia302"
	}

	tokenStorage = "~/.yowsup/t_%s"%(v.replace(".", "_"))
	tokenSource = ("openwhatsapp.org", "/t")

	#t


