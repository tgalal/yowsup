# import auth
# import coder
# import media
# import logger
# import network
# import protocol
# import packetregulator
import unittest
import sys

class YowLayerEvent:
    def __init__(self, name, **kwargs):
        self.name = name
        self.args = kwargs

    def getName(self):
        return self.name

    def getArg(self, name):
        return self.args[name] if name in self.args else None


class YowLayer(object):
    __upper = None
    __lower = None
    _props = {}
    # def __init__(self, upperLayer, lowerLayer):
    #     self.setLayers(upperLayer, lowerLayer)

    def __init__(self):
        super(YowLayer, self).__init__()
        self.setLayers(None, None)

    def setStack(self, stack):
        self.__stack = stack

    def getStack(self):
        return self.__stack

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

    def getProp(self, key, default = None):
        return self.getStack().getProp(key, default)

    def setProp(self, key, val):
        return self.getStack().setProp(key, val)


class YowProtocolLayer(YowLayer):
    def __init__(self, handleMap = {}):
        super(YowProtocolLayer, self).__init__()
        self.handleMap = handleMap

    def receive(self, node):
        if node.tag in self.handleMap:
            recv, _ = self.handleMap[node.tag]
            if recv:
                recv(node)

    def send(self, entity):
        if entity.getTag() in self.handleMap:
            _, send = self.handleMap[entity.getTag()]
            if send:
                send(entity)

    def entityToLower(self, entity):
        #super(YowProtocolLayer, self).toLower(entity.toProtocolTreeNode())
        self.toLower(entity.toProtocolTreeNode())

    def isGroupJid(self, jid):
        return "-" in jid

    def raiseErrorForNode(self, node):
        raise ValueError("Unimplemented notification type %s " % node)

class YowParallelLayer(YowLayer):
    def __init__(self, sublayers = []):
        super(YowParallelLayer, self).__init__()
        self.sublayers = tuple([sublayer() for sublayer in sublayers])
        for s in self.sublayers:
            #s.setLayers(self, self)
            s.toLower = self.toLower
            s.toUpper = self.toUpper
            s.broadcastEvent = self.broadcastEvent
            s.emitEvent = self.emitEvent


    def setStack(self, stack):
        super(YowParallelLayer, self).setStack(stack)
        for s in self.sublayers:
            s.setStack(self.getStack())


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