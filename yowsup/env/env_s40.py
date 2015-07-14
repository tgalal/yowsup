from .env import YowsupEnv
import base64
import hashlib
class S40YowsupEnv(YowsupEnv):
    _VERSION = "2.12.82"
    _OS_NAME= "S40"
    _OS_VERSION = "14.26"
    _DEVICE_NAME = "Nokia302"
    _TOKEN_STRING  = "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1431039885607{phone}"
    _AXOLOTL = False

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
        return hashlib.md5(self.__class__._TOKEN_STRING.format(phone = phoneNumber).encode()).hexdigest()

    def getUserAgent(self):
        return self.__class__._USERAGENT_STRING.format(
            WHATSAPP_VERSION = self.getVersion(),
            OS_NAME = self.getOSName() + "Version",
            OS_VERSION = self.getOSVersion(),
            DEVICE_NAME = self.getDeviceName()
        )

