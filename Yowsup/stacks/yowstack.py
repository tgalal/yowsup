class YowStack:
    __stack = []
    __stackInstances = []
    def __init__(self, stackClassesArr = []):
        self.__stack = stackClassesArr or []
        self.__stackInstances = []

    def addLayer(self, layerClass):
        self.__stack.push(layerClass)

    def addPostConstructLayer(self, layer):
        self.__stackInstances[-1].setLayers(layer, self.__stackInstances[-2])
        layer.setLayers(None, self.__stackInstances[-1])
        self.__stackInstances.append(layer)

    def construct(self):
        print("Initialzing stack")
        for s in self.__stack:
            print("Constructing %s" %s)
            self.__stackInstances.append(s())

        for i in range(0, len(self.__stackInstances)):
            upperLayer = self.__stackInstances[i + 1] if (i + 1) < len(self.__stackInstances) else None
            lowerLayer = self.__stackInstances[i - 1] if i > 0 else None
            self.__stackInstances[i].setLayers(upperLayer, lowerLayer)

    def sendInitSignal(self):
        print("Initialzing layers")
        self.__stackInstances[0].init()