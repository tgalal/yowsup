import base64
import hashlib
import os
class YowConstants:
    DOMAIN       = "s.whatsapp.net"
    RESOURCE     = "Android-2.11.471-443"#"S40-2.12.53"
    ENDPOINTS     = (
        ("c2.whatsapp.net", 443),
        )

    DATA_CLIENT = {
        "v": "2.11.471",
        "r": "Android-2.11.471-443",
        "u": "WhatsApp/2.11.471 Android/4.3 Device/GalaxyS3",#"WhatsApp/2.12.53 S40Version/14.26 Device/Nokia302",
        "t": "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1416435341393{phone}",
        "d": "Android"
    }
    PATH_STORAGE = "~/.yowsup"

    #######ANDROID
    SIGNATURE = "MIIDMjCCAvCgAwIBAgIETCU2pDALBgcqhkjOOAQDBQAwfDELMAkGA1UEBhMCVVMxEzARBgNVBAgTCkNhbGlmb3JuaWExFDASBgNV" \
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

    MD5_CLASSES = "zkrJMO7CuBg3gV4h3ZPrbg=="
    KEY = "/UIGKU1FVQa+ATM2A0za7G2KI9S/CwPYjgAbc67v7ep42eO/WeTLx1lb1cHwxpsEgF4+PmYpLd2YpGUdX/A2JQitsHzDwgcdBpUf7psX1BU="
    @staticmethod
    def generateRequestToken(phone):
        keyDecoded = bytearray(base64.b64decode(YowConstants.KEY))
        sigDecoded = base64.b64decode(YowConstants.SIGNATURE)
        clsDecoded = base64.b64decode(YowConstants.MD5_CLASSES)
        data = sigDecoded + clsDecoded + phone.encode()

        opad = bytearray()
        ipad = bytearray()
        for i in range(0, 64):
            opad.append(0x5C ^ keyDecoded[i])
            ipad.append(0x36 ^ keyDecoded[i])
        hash = hashlib.sha1()
        subHash = hashlib.sha1()
        subHash.update(ipad + data)
        hash.update(opad + subHash.digest())
        result = base64.b64encode(hash.digest())
        return result

