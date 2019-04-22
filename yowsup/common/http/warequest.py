from .waresponseparser import ResponseParser
from yowsup.env import YowsupEnv

import sys
import logging
from axolotl.ecc.curve import Curve
from axolotl.ecc.ec import ECPublicKey
from yowsup.common.tools import WATools
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from yowsup.axolotl.factory import AxolotlManagerFactory
import struct
import random
import base64

if sys.version_info < (3, 0):
    import httplib
    from urllib import quote as urllib_quote

    if sys.version_info >= (2, 7, 9):
        # see https://github.com/tgalal/yowsup/issues/677
        import ssl

        ssl._create_default_https_context = ssl._create_unverified_context

else:
    from http import client as httplib
    from urllib.parse import quote as urllib_quote

logger = logging.getLogger(__name__)


class WARequest(object):
    OK = 200
    ENC_PUBKEY = Curve.decodePoint(
        bytearray([
            5, 142, 140, 15, 116, 195, 235, 197, 215, 166, 134, 92, 108,
            60, 132, 56, 86, 176, 97, 33, 204, 232, 234, 119, 77, 34, 251,
            111, 18, 37, 18, 48, 45
        ])
    )

    def __init__(self, config):
        """
       :type method: str
       :param config:
       :type config: yowsup.config.v1.config.Config
       """

        self.pvars = []
        self.port = 443
        self.type = "GET"
        self.parser = None
        self.params = []
        self.headers = {}

        self.sent = False
        self.response = None

        self._config = config
        self._p_in = str(config.phone)[len(str(config.cc)):]
        self._axolotlmanager = AxolotlManagerFactory() \
            .get_manager(self._config.phone)  # type: yowsup.axolotl.manager.Axolotlmanager

        if config.expid is None:
            config.expid = WATools.generateDeviceId()

        if config.fdid is None:
            config.fdid = WATools.generatePhoneId()

        if config.client_static_keypair is None:
            config.client_static_keypair = WATools.generateKeyPair()

        self.addParam("cc", config.cc)
        self.addParam("in", self._p_in)
        self.addParam("lg", "en")
        self.addParam("lc", "GB")
        self.addParam("mistyped", "6")
        self.addParam("authkey", self.b64encode(config.client_static_keypair.public.data))
        self.addParam("e_regid", self.b64encode(struct.pack('>I', self._axolotlmanager.registration_id)))
        self.addParam("e_keytype", self.b64encode(b"\x05"))
        self.addParam("e_ident", self.b64encode(self._axolotlmanager.identity.publicKey.serialize()[1:]))

        signedprekey = self._axolotlmanager.load_latest_signed_prekey(generate=True)
        self.addParam("e_skey_id", self.b64encode(struct.pack('>I', signedprekey.getId())[1:]))
        self.addParam("e_skey_val", self.b64encode(signedprekey.getKeyPair().publicKey.serialize()[1:]))
        self.addParam("e_skey_sig", self.b64encode(signedprekey.getSignature()))

        self.addParam("fdid", config.fdid)
        self.addParam("expid", self.b64encode(config.expid))

        self.addParam("network_radio_type", "1")
        self.addParam("simnum", "1")
        self.addParam("hasinrc", "1")
        self.addParam("pid", int(random.uniform(100, 9999)))
        self.addParam("rc", 0)
        if self._config.id:
            self.addParam("id", self._config.id)

    def setParsableVariables(self, pvars):
        self.pvars = pvars

    def onResponse(self, name, value):
        if name == "status":
            self.status = value
        elif name == "result":
            self.result = value

    def addParam(self, name, value):
        self.params.append((name, value))

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

    def send(self, parser=None, encrypt=True, preview=False):
        logger.debug("send(parser=%s, encrypt=%s, preview=%s)" % (
            None if parser is None else "[omitted]",
            encrypt, preview
        ))
        if self.type == "POST":
            return self.sendPostRequest(parser)

        return self.sendGetRequest(parser, encrypt, preview=preview)

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

    def encryptParams(self, params, key):
        """
        :param params:
        :type params: list
        :param key:
        :type key: ECPublicKey
        :return:
        :rtype: list
        """
        keypair = Curve.generateKeyPair()
        encodedparams = self.urlencodeParams(params)

        cipher = AESGCM(Curve.calculateAgreement(key, keypair.privateKey))
        ciphertext = cipher.encrypt(b'\x00\x00\x00\x00' + struct.pack('>Q', 0), encodedparams.encode(), b'')

        payload = base64.b64encode(keypair.publicKey.serialize()[1:] + ciphertext)
        return [('ENC', payload)]

    def sendGetRequest(self, parser=None, encrypt_params=True, preview=False):
        logger.debug("sendGetRequest(parser=%s, encrypt_params=%s, preview=%s)" % (
            None if parser is None else "[omitted]",
            encrypt_params, preview
        ))
        self.response = None

        if encrypt_params:
            logger.debug("Encrypting parameters")
            if logger.level <= logging.DEBUG:
                logger.debug("pre-encrypt (encoded) parameters = \n%s", (self.urlencodeParams(self.params)))
            params = self.encryptParams(self.params, self.ENC_PUBKEY)
        else:
            ## params will be logged right before sending
            params = self.params

        parser = parser or self.parser or ResponseParser()

        headers = dict(
            list(
                {
                    "User-Agent": self.getUserAgent(),
                    "Accept": parser.getMeta()
                }.items()
            ) + list(self.headers.items()))

        host, port, path = self.getConnectionParameters()

        self.response = WARequest.sendRequest(host, port, path, headers, params, "GET", preview=preview)

        if preview:
            logger.info("Preview request, skip response handling and return None")
            return None

        if not self.response.status == WARequest.OK:
            logger.error("Request not success, status was %s" % self.response.status)
            return {}

        data = self.response.read()
        logger.info(data)

        self.sent = True
        return parser.parse(data.decode(), self.pvars)

    def sendPostRequest(self, parser=None):
        self.response = None
        params = self.params  # [param.items()[0] for param in self.params];

        parser = parser or self.parser or ResponseParser()

        headers = dict(list({"User-Agent": self.getUserAgent(),
                             "Accept": parser.getMeta(),
                             "Content-Type": "application/x-www-form-urlencoded"
                             }.items()) + list(self.headers.items()))

        host, port, path = self.getConnectionParameters()
        self.response = WARequest.sendRequest(host, port, path, headers, params, "POST")

        if not self.response.status == WARequest.OK:
            logger.error("Request not success, status was %s" % self.response.status)
            return {}

        data = self.response.read()

        logger.info(data)

        self.sent = True
        return parser.parse(data.decode(), self.pvars)

    def b64encode(self, value):
        return base64.urlsafe_b64encode(value).replace(b'=', b'')

    @classmethod
    def urlencode(cls, value):
        if type(value) not in (str, bytes):
            value = str(value)

        out = ""
        for char in value:
            if type(char) is int:
                char = bytearray([char])
            quoted = urllib_quote(char, safe='')
            out += quoted if quoted[0] != '%' else quoted.lower()

        return out \
            .replace('-', '%2d') \
            .replace('_', '%5f') \
            .replace('~', '%7e')

    @classmethod
    def urlencodeParams(cls, params):
        merged = []
        for k, v in params:
            merged.append(
                "%s=%s" % (k, cls.urlencode(v))
            )
        return "&".join(merged)

    @classmethod
    def sendRequest(cls, host, port, path, headers, params, reqType="GET", preview=False):
        logger.debug("sendRequest(host=%s, port=%s, path=%s, headers=%s, params=%s, reqType=%s, preview=%s)" % (
            host, port, path, headers, params, reqType, preview
        ))

        params = cls.urlencodeParams(params)

        path = path + "?" + params if reqType == "GET" and params else path

        if not preview:
            logger.debug("Opening connection to %s" % host)
            conn = httplib.HTTPSConnection(host, port) if port == 443 else httplib.HTTPConnection(host, port)
        else:
            logger.debug("Should open connection to %s, but this is a preview" % host)
            conn = None

        if not preview:
            logger.debug("Sending %s request to %s" % (reqType, path))
            conn.request(reqType, path, params, headers)
        else:
            logger.debug("Should send %s request to %s, but this is a preview" % (reqType, path))
            return None

        response = conn.getresponse()
        return response
