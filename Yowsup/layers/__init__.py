# import auth
# import coder
# import media
# import logger
# import network
# import protocol
# import packetregulator
import unittest

class YowLayerEvent:
    def __init__(self, name, **kwargs):
        self.name = name
        self.args = kwargs

    def getName(self):
        return self.name


class YowLayer(object):
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

    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        self.toUpper(data)

    def toUpper(self, data):
        if self.__upper:
            self.__upper.receive(data)

    def toLower(self, data):
        if self.__lower:
            self.__lower.send(data)

    def emitEvent(self, yowLayerEvent):
        if self.__upper and not self.__upper.onEvent(yowLayerEvent):
            self.__upper.emitEvent(yowLayerEvent)

    def broadcastEvent(self, yowLayerEvent):
        if self.__lower and not self.__lower.onEvent(yowLayerEvent):
            self.__lower.broadcastEvent(yowLayerEvent)

    '''return true to stop propagating the event'''
    def onEvent(self, yowLayerEvent):
        return False


    @classmethod
    def setProp(cls, key, value):
        cls._props[key] = value

    @classmethod
    def getProp(cls, key, default = None):
        return cls._props[key] if key in cls._props else default


class YowProtocolLayer(YowLayer):
    def __init__(self, recvHandleMap = {}):
        super(YowProtocolLayer, self).__init__()
        self.recvHandleMap = recvHandleMap

    def receive(self, node):
        if node.tag in self.recvHandleMap:
            self.recvHandleMap[node.tag](node)

    def toLower(self, entity):
        super(YowProtocolLayer, self).toLower(entity.toProtocolTreeNode())

    def isGroupJid(self, jid):
        return "-" in jid

class YowParallelLayer(YowLayer):
    def __init__(self, sublayers = []):
        super(YowParallelLayer, self).__init__()
        self.sublayers = tuple([sublayer() for sublayer in sublayers])
        for s in self.sublayers:
            #s.setLayers(self, self)
            s.toLower = self.toLower
            s.toUpper = self.toUpper


    def receive(self, data):
        for s in self.sublayers:
            s.receive(data)

    def send(self, data):
        for s in self.sublayers:
            s.send(data)


    def onEvent(self, yowLayerEvent):
        stopEvent = False
        for s in self.sublayers:
            stopEvent = stopEvent or s.onEvent(yowLayerEvent)

        return stopEvent

    def __str__(self):
        return " - ".join([l.__str__() for l in self.sublayers])


class YowLayerTest(unittest.TestCase):
    def __init__(self, *args):
        super(YowLayerTest, self).__init__(*args)
        self.dataSink = None
        self.toUpper = self.receiveOverrider
        self.toLower = self.sendOverrider

    def receiveOverrider(self, data):
        self.dataSink = data

    def sendOverrider(self, data):
        self.dataSink = data

    def targetReceive(self, data):
        self.targetLayer.receive(data)

    def targetSend(self, data):
        self.targetLayer.send(data)


    def setTargetLayer(self, targetLayer):
        self.targetLayer = targetLayer
        self.targetLayer.setLayers(self.sinkLayer, self.sinkLayer)
        self.sinkLayer.setLayers(self.targetLayer, self.targetLayer)