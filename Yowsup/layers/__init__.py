# import auth
# import coder
# import media
# import logger
# import network
# import protocol
# import packetregulator


class YowLayer:
    __upper = None
    __lower = None
    _props = {}
    # def __init__(self, upperLayer, lowerLayer):
    #     self.setLayers(upperLayer, lowerLayer)

    def __init__(self):
        self.setLayers(None, None)

    def setLayers(self, upper, lower):
        self.__upper = upper
        self.__lower = lower

    def init(self):
        self.initUpper()
        return True

    def send(self, data):
        pass

    def receive(self, data):
        pass

    def toUpper(self, data):
        if self.__upper:
            self.__upper.receive(data)

    def toLower(self, data):
        if self.__lower:
            self.__lower.send(data)

    @classmethod
    def setProp(cls, key, value):
        cls._props[key] = value

    @classmethod
    def getProp(cls, key, default = None):
        return cls._props[key] if key in cls._props else default

    def initUpper(self):
        if self.__upper:
            self.__upper.init()

class YowParallelLayer(YowLayer):
    def __init__(self, parallerLayers):
        self.parallerLayers = []
        for p in  parallerLayers:
            pInst = p()
            pInst.setLayers(self, self)
            self.parallerLayers.append(p)


    def send(self, data):


    def receive(self, data):
        