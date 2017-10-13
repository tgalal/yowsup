import urllib,sys, os, logging
import hashlib
from .waresponseparser import ResponseParser
from yowsup.env import YowsupEnv
from .httpproxy import HttpProxy

if sys.version_info < (3, 0):
    import httplib
    from urllib import urlencode

    if sys.version_info >= (2, 7, 9):
        #see https://github.com/tgalal/yowsup/issues/677
        import ssl
        ssl._create_default_https_context = ssl._create_unverified_context

else:
    from http import client as httplib
    from urllib.parse import urlencode

logger = logging.getLogger(__name__)


class WARequest(object):

    OK = 200

    def __init__(self):

        self.pvars = []
        self.port = 443
        self.type = "GET"
        self.parser = None
        self.params = []
        self.headers = {}

        self.sent = False
        self.response = None

    def setParsableVariables(self, pvars):
        self.pvars = pvars

    def onResponse(self, name, value):
        if name == "status":
            self.status = value
        elif name == "result":
            self.result = value

    def addParam(self,name,value):
        self.params.append((name,value))

    def removeParam(self, name):
        for i in range(0, len(self.params)):
            if self.params[i][0] == name:
                del self.params[i]


    def addHeaderField(self, name, value):
        self.headers[name] = value

    def clearParams(self):
        self.params = []

    def getUserAgent(self):
        return YowsupEnv.getCurrent().getUserAgent()

    def send(self, parser = None):

        if self.type == "POST":
            return self.sendPostRequest(parser)

        return self.sendGetRequest(parser)

    def setParser(self, parser):
        if isinstance(parser, ResponseParser):
            self.parser = parser
        else:
            logger.error("Invalid parser")

    def getConnectionParameters(self):

        if not self.url:
            return "", "", self.port

        try:
            url = self.url.split("://", 1)
            url = url[0] if len(url) == 1 else url[1]

            host, path = url.split('/', 1)
        except ValueError:
            host = url
            path = ""

        path = "/" + path

        return host, self.port, path

    def sendGetRequest(self, parser = None):
        self.response = None
        params =  self.params#[param.items()[0] for param in self.params];

        parser = parser or self.parser or ResponseParser()

        headers = dict(list({"User-Agent":self.getUserAgent(),
                "Accept": parser.getMeta()
            }.items()) + list(self.headers.items()));

        host,port,path = self.getConnectionParameters()
        proxy = HttpProxy.getFromEnviron()
        if proxy is None:
            self.response = WARequest.sendRequest(host, port, path, headers, params, "GET")

            if not self.response.status == WARequest.OK:
                logger.error("Request not success, status was %s"%self.response.status)
                return {}

            data = self.response.read()
            logger.info(data)

            self.sent = True
            return parser.parse(data.decode(), self.pvars)
        else:
            logger.info("Request with proxy")
            self.response = WARequest.sendRequestWithProxy(host, port,path,headers, params, proxy)
            logger.info(self.response)
            return self.response
            

    def sendPostRequest(self, parser = None):
        self.response = None
        params =  self.params #[param.items()[0] for param in self.params];

        parser = parser or self.parser or ResponseParser()

        headers = dict(list({"User-Agent":self.getUserAgent(),
                "Accept": parser.getMeta(),
                "Content-Type":"application/x-www-form-urlencoded"
            }.items()) + list(self.headers.items()))

        host,port,path = self.getConnectionParameters()
        self.response = WARequest.sendRequest(host, port, path, headers, params, "POST")


        if not self.response.status == WARequest.OK:
            logger.error("Request not success, status was %s" % self.response.status)
            return {}

        data = self.response.read()

        logger.info(data)

        self.sent = True
        return parser.parse(data.decode(), self.pvars)


    @staticmethod
    def sendRequest(host, port, path, headers, params, reqType="GET"):

        params = urlencode(params)


        path = path + "?"+ params if reqType == "GET" and params else path

        if len(headers):
            logger.debug(headers)
        if len(params):
            logger.debug(params)

        logger.debug("Opening connection to %s" % host);
        conn = httplib.HTTPSConnection(host ,port) if port == 443 else httplib.HTTPConnection(host ,port)

        logger.debug("Sending %s request to %s" % (reqType, path))
        conn.request(reqType, path, params, headers);

        response = conn.getresponse()
        return response

    def sendRequestWithProxy(host,port,path,headers,params,proxy):
        import pycurl
        import json
        from io import BytesIO
        logger.info("SENDING PROXY REQUEST WITH %s"%proxy.getHost())
        bytes_buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(pycurl.URL, WARequest.build_get_url(host,path,params))
        c.setopt(pycurl.PROXY,proxy.getHost())
        c.setopt(pycurl.PROXYPORT,proxy.getPort())
        if proxy.getUserName() is not None:
            c.setopt(pycurl.PROXYUSERPWD, "%s:%s" % (proxy.getUser(), proxy.getPassword()))
        c.setopt(pycurl.PORT, port)
        c.setopt(pycurl.HTTPHEADER,WARequest.build_headers(headers))
        c.setopt(pycurl.WRITEDATA, bytes_buffer)
        c.perform()
        c.close()
        data = bytes_buffer.getvalue().decode('utf-8')
        return json.loads(data)

    @staticmethod
    def build_get_url(host, path, params):
        params = urlencode(params)
        url = 'https://'+host+path+"?"+params 
        print(url)
        return url 
        
    @staticmethod
    def build_headers(headers_tuple):
        headers_array = []
        for idx in headers_tuple:
            headers_array.append(idx + ":"+headers_tuple[idx])
        print(headers_array)
        return headers_array

