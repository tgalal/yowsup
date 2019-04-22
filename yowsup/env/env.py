import abc
import logging
from six import with_metaclass

logger = logging.getLogger(__name__)

DEFAULT = "android"


class YowsupEnvType(abc.ABCMeta):
    def __init__(cls, name, bases, dct):
        if name != "YowsupEnv":
            YowsupEnv.registerEnv(cls)
        super(YowsupEnvType, cls).__init__(name, bases, dct)


class YowsupEnv(with_metaclass(YowsupEnvType, object)):
    __metaclass__ = YowsupEnvType
    __ENVS = {}
    __CURR = None

    _USERAGENT_STRING = "WhatsApp/{WHATSAPP_VERSION} {OS_NAME}/{OS_VERSION} Device/{MANUFACTURER}-{DEVICE_NAME}"

    @classmethod
    def registerEnv(cls, envCls):
        envName = envCls.__name__.lower().replace("yowsupenv", "")
        cls.__ENVS[envName] = envCls
        logger.debug("registered env %s => %s" % (envName, envCls))

    @classmethod
    def setEnv(cls, envName):
        if not envName in cls.__ENVS:
            raise ValueError("%s env does not exist" % envName)
        logger.debug("Current env changed to %s " % envName)
        cls.__CURR = cls.__ENVS[envName]()

    @classmethod
    def getEnv(cls, envName):
        if not envName in cls.__ENVS:
            raise ValueError("%s env does not exist" % envName)

        return cls.__ENVS[envName]()

    @classmethod
    def getRegisteredEnvs(cls):
        return list(cls.__ENVS.keys())

    @classmethod
    def getCurrent(cls):
        """
        :rtype: YowsupEnv
        """
        if cls.__CURR is None:
            env = DEFAULT
            envs = cls.getRegisteredEnvs()
            if env not in envs:
                env = envs[0]
            logger.debug("Env not set, setting it to %s" % env)
            cls.setEnv(env)
        return cls.__CURR

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
    def getManufacturer(self):
        pass

    def getBuildVersion(self):
        pass

    def getUserAgent(self):
        return self.__class__._USERAGENT_STRING.format(
            WHATSAPP_VERSION=self.getVersion(),
            OS_NAME=self.getOSName(),
            OS_VERSION=self.getOSVersion(),
            MANUFACTURER=self.getManufacturer(),
            DEVICE_NAME=self.getDeviceName()
        )
