from .env import YowsupEnv
import hashlib
class S40YowsupEnv(YowsupEnv):
    _VERSION = "2.16.7"
    _OS_NAME= "S40"
    _OS_VERSION = "14.26"
    _DEVICE_NAME = "302"
    _MANUFACTURER = "Nokia"
    _TOKEN_STRING  = "PdA2DJyKoUrwLw1Bg6EIhzh502dF9noR9uFCllGk1462212402694{phone}"
    _AXOLOTL = True

    def getVersion(self):
        return self.__class__._VERSION

    def getOSName(self):
        return self.__class__._OS_NAME

    def getOSVersion(self):
        return self.__class__._OS_VERSION

    def getDeviceName(self):
        return self.__class__._DEVICE_NAME

    def getManufacturer(self):
        return self.__class__._MANUFACTURER

    def isAxolotlEnabled(self):
        return self.__class__._AXOLOTL

    def getToken(self, phoneNumber):
        return hashlib.md5(self.__class__._TOKEN_STRING.format(phone = phoneNumber).encode()).hexdigest()

    def getUserAgent(self):
        return self.__class__._USERAGENT_STRING.format(
            WHATSAPP_VERSION = self.getVersion(),
            OS_NAME = self.getOSName() + "Version",
            OS_VERSION = self.getOSVersion(),
            DEVICE_NAME = self.getDeviceName(),
            MANUFACTURER = self.getManufacturer()
        )
