from Yowsup.layers import YowParallelLayer
class YowStack(object):
    __stack = []
    __stackInstances = []
    def __init__(self, stackClassesArr = ()):
        self.__stack = stackClassesArr[::-1] or []
        self.__stackInstances = []
        self._construct()

    def addLayer(self, layerClass):
        self.__stack.push(layerClass)

    def addPostConstructLayer(self, layer):
        self.__stackInstances[-1].setLayers(layer, self.__stackInstances[-2])
        layer.setLayers(None, self.__stackInstances[-1])
        self.__stackInstances.append(layer)

    def _construct(self):
        print("Initialzing stack")
        for s in self.__stack:
            if type(s) is tuple:
                inst = YowParallelLayer(s)
            else:
                inst = s()
            print("Constructed %s" % inst)
            self.__stackInstances.append(inst)

        for i in range(0, len(self.__stackInstances)):
            upperLayer = self.__stackInstances[i + 1] if (i + 1) < len(self.__stackInstances) else None
            lowerLayer = self.__stackInstances[i - 1] if i > 0 else None
            self.__stackInstances[i].setLayers(upperLayer, lowerLayer)

    def getLayer(self, layerIndex):
        return self.__stackInstances[layerIndex]

