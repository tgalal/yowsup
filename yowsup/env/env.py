import abc
class YowsupEnv(object):
    __metaclass__ = abc.ABCMeta

    _USERAGENT_STRING = "WhatsApp/{WHATSAPP_VERSION} {OS_NAME}/{OS_VERSION} Device/{DEVICE_NAME}"

    @abc.abstractmethod
    def getToken(self, phoneNumber):
        pass

    @abc.abstractmethod
    def getVersion(self):
        pass

    @abc.abstractmethod
    def getOSVersion(self):
        pass

    @abc.abstractmethod
    def getOSName(self):
        pass

    @abc.abstractmethod
    def getDeviceName(self):
        pass

    @abc.abstractmethod
    def isAxolotlEnabled(self):
        pass

    def getResource(self):
        return self.getOSName() + "-" + self.getVersion()

    def getUserAgent(self):
        return self.__class__._USERAGENT_STRING.format(
            WHATSAPP_VERSION = self.getVersion(),
            OS_NAME = self.getOSName(),
            OS_VERSION = self.getOSVersion(),
            DEVICE_NAME = self.getDeviceName()
        )

