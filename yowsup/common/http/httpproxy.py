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

import os, base64

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class HttpProxy:
    
    instance = None

    def __init__(self, address, username = None, password = None):
        self.address = address
        self.username = username
        self.password = password

    def __repr__(self):
        return repr(self.address)

    def handler(self):
        return HttpProxyHandler(self)

    @staticmethod
    def setProxy(address, port=443, username = None, password = None):
       proxy = HttpProxy((address,port),username, password)
       HttpProxy.instance = proxy

    @staticmethod
    def getFromEnviron():
        if HttpProxy.instance is not None:
            return HttpProxy.instance
        url = None
        for key in ('http_proxy', 'https_proxy'):
            url = os.environ.get(key)
            if url: break
        if not url:
            return None
        dat = urlparse(url)
        port = 80 if dat.scheme == 'http' else 443
        if dat.port != None: port = int(dat.port)
        host = dat.hostname
        return HttpProxy((host, port), dat.username, dat.password)

    def getHost(self):
        return self.address[0]

    def getPort(self):
        return self.address[1]

    def getUserName(self):
        return self.username

    def getPassword(self):
        return self.password

class HttpProxyHandler:

    def __init__(self, proxy):
        self.state = 'init'
        self.proxy = proxy

    def onConnect(self):
        pass

    def connect(self, socket, pair):
        proxy = self.proxy
        authHeader = None
        if proxy.username and proxy.password:
            key = bytes(proxy.username, 'ascii') + b':' + bytes(proxy.password, 'ascii') if (bytes != str) else bytes(proxy.username) + b':' + proxy.password
            auth = base64.b64encode(key)
            authHeader = b'Proxy-Authorization: Basic ' + auth + b'\r\n'
        data = bytearray('CONNECT %s:%d HTTP/1.1\r\nHost: %s:%d\r\n' % (2 * pair), 'ascii')
        if authHeader:
            data += authHeader
        data += b'\r\n'
        self.state = 'connect'
        self.data = data
        socket.connect(proxy.address)

    def send(self, socket):
        if self.state == 'connect':
            socket.send(self.data)
            self.state = 'sent'

    def recv(self, socket, size):
        if self.state == 'sent':
            data = socket.recv(size)
            data = data.decode('ascii')
            status = data.split(' ', 2)
            if status[1] != '200':
                raise Exception('%s' % (data[:data.index('\r\n')]))
            self.state = 'end'
            self.onConnect()
            return data
