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

import hashlib, string, os, base64, ast, sys
from Yowsup.Common.constants import Constants
class Utilities:

	tokenCacheEnabled = True

	@staticmethod
	def processIdentity(identifier):
		try:
			identifier.index(":")
			identifier = identifier.upper()
			identifier = identifier + identifier

		except:
			identifier = identifier[::-1]

		digest = hashlib.md5(identifier.encode("utf-8"))
		return digest.hexdigest()

	@staticmethod
	def decodeString(encoded):
		return "".join(map(chr,  map(lambda x: x ^ 19, encoded)))


	@staticmethod
	def persistToken(token):
		tPath = os.path.expanduser(Constants.tokenStorage)
		dirname = os.path.dirname(tPath)

		if not os.path.exists(dirname):
			os.makedirs(dirname)

		with open(tPath, "w") as out:
			out.write(base64.b64encode(token).decode())

	@staticmethod
	def readToken():
		if not Utilities.tokenCacheEnabled:
			return None

		token = None
		tPath = os.path.expanduser(Constants.tokenStorage)

		if os.path.exists(tPath):
			with open(tPath, "r") as f:
				tdec = base64.b64decode(f.readline().encode()).decode()
				token = ast.literal_eval(tdec)

		return token

	@staticmethod
	def str( number, radix ):
		"""str( number, radix ) -- reverse function to int(str,radix) and long(str,radix)"""

		if not 2 <= radix <= 36:
			raise ValueError("radix must be in 2..36")

		abc = string.digits + string.ascii_letters

		result = ''

		if number < 0:
			number = -number
			sign = '-'
		else:
			sign = ''

		while True:
			number, rdigit = divmod( number, radix )
			result = abc[rdigit] + result
			if number == 0:
				return sign + result
