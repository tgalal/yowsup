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
from hashlib import md5
import random, sys
from Yowsup.Common.utilities import Utilities

class WAContactsSyncRequest():

    def __init__(self, username, password, contacts):
        
        self.username = username
        self.password = password
        
        self.contacts = contacts
        self.authReq = WAContactsSyncAuth(username, password)
        
    def setCredentials(self, username, password):
        self.username = username
        self.password = password
        self.authReq = WAContactsSyncAuth(username, password)
        
    def setContacts(self, contacts):
        self.contacts = contacts
        
    def send(self):
        auth = self.authReq.send()
        
        if not auth["message"] == "next token":
            return auth
        
        response = self.authReq.response
        
        respH = response.getheader("www-authenticate")
        
        self.authReq._d(respH)
        
        tmp = respH[respH.index('nonce="')+len('nonce="'):]
        nonce = tmp[:tmp.index('"')]
        
        q = WAContactsSyncQuery(self.username, self.password, nonce, self.contacts)
        
        resp = q.send()
        
        return resp
        
        
        
class WAContactsSyncAuth(WARequest):
    
    nc = "00000001"
    realm = "s.whatsapp.net"
    qop = "auth"
    digestUri = "WAWA/s.whatsapp.net"
    charSet = "utf-8"
    authMethod = "X-WAWA"
    
    authTemplate = '{auth_method}: username="{username}",realm="{realm}",nonce="{nonce}",cnonce="{cnonce}",nc="{nc}",qop="auth",\
digest-uri="{digest_uri}",response="{response}",charset="utf-8"'
    
    def __init__(self, username, password, nonce = "0"):
        
        super(WAContactsSyncAuth, self).__init__();
        self.url = "sro.whatsapp.net/v2/sync/a"
        self.type = "POST"
        cnonce = Utilities.str(random.randint(100000000000000,1000000000000000), 36)
        
        credentials = bytearray((username+":s.whatsapp.net:").encode())
        credentials.extend(password)

        if sys.version_info >= (3, 0):
            buf = lambda x: bytes(x, 'iso-8859-1') if type(x) is str else bytes(x)
        else:
            buf = buffer
        

        response = self.encode(
                        self.md5(
                            self.encode(
                                self.md5(
                                    self.md5( buf ( credentials ) ) 
                                        + (":" + nonce + ":" + cnonce).encode()  
                                    )
                                )
                                 + (":"+nonce+":" + WAContactsSyncAuth.nc+":" + cnonce + ":auth:").encode()
                                + self.encode(
                                        self.md5(("AUTHENTICATE:"+WAContactsSyncAuth.digestUri).encode())
                                ))).decode()
        
        
        
        authField = WAContactsSyncAuth.authTemplate.format(auth_method = WAContactsSyncAuth.authMethod,
                                                           username = username,
                                                           realm = WAContactsSyncAuth.realm,
                                                           nonce = nonce,
                                                           cnonce = cnonce,
                                                           nc= WAContactsSyncAuth.nc,
                                                           digest_uri = WAContactsSyncAuth.digestUri,
                                                           response = response)
        
        self.addHeaderField("Authorization", authField)        

        self.pvars = ["message"]
        
        self.setParser(JSONResponseParser())
        
        
    def md5(self, data):
        return md5(data).digest();
        
    def getResponseDigest(self):
        pass
    
    def encode(self, inp):
        res = []
        
        
        def _enc(n):
            if n < 10:
                return n + 48
            return n + 87
        
        for c in inp:
            
            if type(inp) is str:
                c = ord(c)
            
            if c < 0: c += 256
            
            res.append(_enc(c >> 4))
            res.append(_enc(c % 16))
        
        
        return "".join(map(chr, res)).encode();
    
    
class WAContactsSyncQuery(WAContactsSyncAuth):
    def __init__(self, username, password, nonce, contacts):
        
        super(WAContactsSyncQuery, self).__init__(username, password, nonce)
        
        
        self.url = "sro.whatsapp.net/v2/sync/q"
        
        self.pvars = ["c"]
        
        
        self.addParam("ut", "all")
        #self.addParam("ut", "wa")
        self.addParam("t", "c")
        #self.addParam("t", "w")
        
        for c in contacts:
            self.addParam("u[]", c)
