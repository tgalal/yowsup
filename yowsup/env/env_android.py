from .env import YowsupEnv
import base64
import hashlib


class AndroidYowsupEnv(YowsupEnv):
    _SIGNATURE = "MIIDMjCCAvCgAwIBAgIETCU2pDALBgcqhkjOOAQDBQAwfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFDASBgNV" \
        "BAcTC1NhbnRhIENsYXJhMRYwFAYDVQQKEw1XaGF0c0FwcCBJbmMuMRQwEgYDVQQLEwtFbmdpbmVlcmluZzEUMBIGA1UEAxMLQnJ" \
        "pYW4gQWN0b24wHhcNMTAwNjI1MjMwNzE2WhcNNDQwMjE1MjMwNzE2WjB8MQswCQYDVQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5" \
        "pYTEUMBIGA1UEBxMLU2FudGEgQ2xhcmExFjAUBgNVBAoTDVdoYXRzQXBwIEluYy4xFDASBgNVBAsTC0VuZ2luZWVyaW5nMRQwEg" \
        "YDVQQDEwtCcmlhbiBBY3RvbjCCAbgwggEsBgcqhkjOOAQBMIIBHwKBgQD9f1OBHXUSKVLfSpwu7OTn9hG3UjzvRADDHj+AtlEm" \
        "aUVdQCJR+1k9jVj6v8X1ujD2y5tVbNeBO4AdNG/yZmC3a5lQpaSfn+gEexAiwk+7qdf+t8Yb+DtX58aophUPBPuD9tPFHsMCN" \
        "VQTWhaRMvZ1864rYdcq7/IiAxmd0UgBxwIVAJdgUI8VIwvMspK5gqLrhAvwWBz1AoGBAPfhoIXWmz3ey7yrXDa4V7l5lK+7+jr" \
        "qgvlXTAs9B4JnUVlXjrrUWU/mcQcQgYC0SRZxI+hMKBYTt88JMozIpuE8FnqLVHyNKOCjrh4rs6Z1kW6jfwv6ITVi8ftiegEkO" \
        "8yk8b6oUZCJqIPf4VrlnwaSi2ZegHtVJWQBTDv+z0kqA4GFAAKBgQDRGYtLgWh7zyRtQainJfCpiaUbzjJuhMgo4fVWZIvXHaS" \
        "HBU1t5w//S0lDK2hiqkj8KpMWGywVov9eZxZy37V26dEqr/c2m5qZ0E+ynSu7sqUD7kGx/zeIcGT0H+KAVgkGNQCo5Uc0koLRW" \
        "YHNtYoIvt5R3X6YZylbPftF/8ayWTALBgcqhkjOOAQDBQADLwAwLAIUAKYCp0d6z4QQdyN74JDfQ2WCyi8CFDUM4CaNB+ceVXd" \
        "KtOrNTQcc0e+t"

    _MD5_CLASSES = "7UDPOXwpiLBvEjT8uNwsuA=="
    _KEY = "eQV5aq/Cg63Gsq1sshN9T3gh+UUp0wIw0xgHYT1bnCjEqOJQKCRrWxdAe2yvsDeCJL+Y4G3PRD2HUF7oUgiGo8vGlNJOaux26k+A2F3hj8A="

    _VERSION = "2.12.440"
    _OS_NAME = "Android"
    _OS_VERSION = "4.3"
    _DEVICE_NAME = "GalaxyS3"
    _AXOLOTL = True

    def getVersion(self):
        return self.__class__._VERSION

    def getOSName(self):
        return self.__class__._OS_NAME

    def getOSVersion(self):
        return self.__class__._OS_VERSION

    def getDeviceName(self):
        return self.__class__._DEVICE_NAME

    def isAxolotlEnabled(self):
        return self.__class__._AXOLOTL

    def getToken(self, phoneNumber):
        keyDecoded = bytearray(base64.b64decode(self.__class__._KEY))
        sigDecoded = base64.b64decode(self.__class__._SIGNATURE)
        clsDecoded = base64.b64decode(self.__class__._MD5_CLASSES)
        data = sigDecoded + clsDecoded + phoneNumber.encode()

        opad = bytearray()
        ipad = bytearray()
        for i in range(0, 64):
            opad.append(0x5C ^ keyDecoded[i])
            ipad.append(0x36 ^ keyDecoded[i])
        hash = hashlib.sha1()
        subHash = hashlib.sha1()
        try:
            subHash.update(ipad + data)
            hash.update(opad + subHash.digest())
        except TypeError:
            subHash.update(bytes(ipad + data))
            hash.update(bytes(opad + subHash.digest()))
        result = base64.b64encode(hash.digest())
        return result
