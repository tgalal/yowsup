from .env import YowsupEnv
import base64
import hashlib


class iOsYowsupEnv(YowsupEnv):
    _VERSION = "2.22.16.77" # 2.20.206.24
    _OS_NAME = "iOS"
    _OS_VERSION = "15.3.1"
    _DEVICE_NAME = "iPhone 7"
    _MANUFACTURER = "Apple"
    _BUILD_VERSION = "19D52"
    _AXOLOTL = True
    _TOKEN = "0a1mLfGUIBVrMKF1RdvLI5lkRBvof6vn0fD2QRSM785a343e772d0c64ec999e7505ffdeaf{phone}"

    def getVersion(self):
        return self.__class__._VERSION

    def getOSName(self):
        return self.__class__._OS_NAME

    def getOSVersion(self):
        return self.__class__._OS_VERSION

    def getDeviceName(self):
        return self.__class__._DEVICE_NAME

    def getBuildVersion(self):
        return self.__class__._BUILD_VERSION

    def getManufacturer(self):
        return self.__class__._MANUFACTURER

    def isAxolotlEnabled(self):
        return self.__class__._AXOLOTL

    def getToken(self, phoneNumber):
        result = hashlib.md5(self.__class__._TOKEN.format(phone = phoneNumber).encode()).hexdigest()
        return result