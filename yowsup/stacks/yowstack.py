from yowsup.layers import YowParallelLayer
import asyncore, time, logging

logger = logging.getLogger(__name__)

class YowStack(object):
    __stack = []
    __stackInstances = []
    def __init__(self, stackClassesArr = ()):
        self.__stack = stackClassesArr[::-1] or []
        self.__stackInstances = []
        self._construct()
        self._props = {}

    def addLayer(self, layerClass):
        self.__stack.push(layerClass)

    def addPostConstructLayer(self, layer):
        self.__stackInstances[-1].setLayers(layer, self.__stackInstances[-2])
        layer.setLayers(None, self.__stackInstances[-1])
        self.__stackInstances.append(layer)

    def setProp(self, key, value):
        self._props[key] = value

    def getProp(self, key, default = None):
        return self._props[key] if key in self._props else default

    def emitEvent(self, yowLayerEvent):
       self.__stackInstances[0].emitEvent(yowLayerEvent)

    def broadcastEvent(self, yowLayerEvent):
        if not self.__stackInstances[-1].onEvent(yowLayerEvent):
            self.__stackInstances[-1].broadcastEvent(yowLayerEvent)

    def loop(self, *args, **kwargs):
        if "discrete" in kwargs:
            discreteVal = kwargs["discrete"]
            del kwargs["discrete"]
            while True:
                asyncore.loop(*args, **kwargs)
                time.sleep(discreteVal)
        else:
            asyncore.loop(*args, **kwargs)

    def _construct(self):
        logger.debug("Initializing stack")
        for s in self.__stack:
            if type(s) is tuple:
                inst = YowParallelLayer(s)
            else:
                inst = s()
            logger.debug("Constructed %s" % inst)
            inst.setStack(self)
            self.__stackInstances.append(inst)

        for i in range(0, len(self.__stackInstances)):
            upperLayer = self.__stackInstances[i + 1] if (i + 1) < len(self.__stackInstances) else None
            lowerLayer = self.__stackInstances[i - 1] if i > 0 else None
            self.__stackInstances[i].setLayers(upperLayer, lowerLayer)

    def getLayer(self, layerIndex):
        return self.__stackInstances[layerIndex]

