from yowsup.layers import YowParallelLayer
import asyncore, time, logging
from yowsup.layers import YowLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.layers.protocol_ib                 import YowIbProtocolLayer
from yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_contacts           import YowContactsIqProtocolLayer
from yowsup.layers.protocol_chatstate          import YowChatstateProtocolLayer
from yowsup.layers.protocol_privacy            import YowPrivacyProtocolLayer
from yowsup.layers.protocol_profiles           import YowProfilesProtocolLayer
from yowsup.layers.axolotl import YowAxolotlLayer
from yowsup.layers.protocol_calls import YowCallsProtocolLayer
from yowsup import env
from yowsup.common.constants import YowConstants
import inspect
try:
    import Queue
except ImportError:
    import queue as Queue
logger = logging.getLogger(__name__)


YOWSUP_PROTOCOL_LAYERS_BASIC = (
    YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
    YowReceiptProtocolLayer, YowAckProtocolLayer, YowPresenceProtocolLayer,
    YowIbProtocolLayer, YowIqProtocolLayer, YowNotificationsProtocolLayer,
    YowContactsIqProtocolLayer, YowChatstateProtocolLayer, YowCallsProtocolLayer

)

class YowStackBuilder(object):

    def __init__(self):
        self.layers = ()

    def pushDefaultLayers(self, axolotl = False):
        defaultLayers = YowStackBuilder.getDefaultLayers(axolotl)
        self.layers += defaultLayers
        return self

    def push(self, yowLayer):
        self.layers += (yowLayer,)
        return self

    def pop(self):
        self.layers = self.layers[:-1]
        return self

    def build(self):
        return YowStack(self.layers, reversed = False)

    @staticmethod
    def getDefaultLayers(axolotl = False, groups = True, media = True, privacy = True, profiles = True):
        coreLayers = YowStackBuilder.getCoreLayers()
        protocolLayers = YowStackBuilder.getProtocolLayers(groups = groups, media=media, privacy=privacy, profiles=profiles)

        allLayers = coreLayers
        if axolotl:
            allLayers += (YowAxolotlLayer,)

        allLayers += (YowParallelLayer(protocolLayers),)

        return allLayers

    @staticmethod
    def getDefaultStack(layer = None, axolotl = False, groups = True, media = True, privacy = True, profiles = True):
        """
        :param layer: An optional layer to put on top of default stack
        :param axolotl: E2E encryption enabled/ disabled
        :return: YowStack
        """

        allLayers = YowStackBuilder.getDefaultLayers(axolotl, groups = groups, media=media,privacy=privacy, profiles=profiles)
        if layer:
            allLayers = allLayers + (layer,)


        return YowStack(allLayers, reversed = False)

    @staticmethod
    def getCoreLayers():
        return (
            YowLoggerLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )[::-1]

    @staticmethod
    def getProtocolLayers(groups = True, media = True, privacy = True, profiles = True):
        layers = YOWSUP_PROTOCOL_LAYERS_BASIC
        if groups:
            layers += (YowGroupsProtocolLayer,)

        if media:
            layers += (YowMediaProtocolLayer, )

        if privacy:
            layers += (YowPrivacyProtocolLayer, )

        if profiles:
            layers += (YowProfilesProtocolLayer, )

        return layers

class YowStack(object):
    __stack = []
    __stackInstances = []
    __detachedQueue = Queue.Queue()
    def __init__(self, stackClassesArr = None, reversed = True):
        stackClassesArr = stackClassesArr or ()
        self.__stack = stackClassesArr[::-1] if reversed else stackClassesArr
        self.__stackInstances = []
        self._construct()
        self._props = {}

        self.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())


    def setCredentials(self, credentials):
        self.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)

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
        if not self.__stackInstances[0].onEvent(yowLayerEvent):
            self.__stackInstances[0].emitEvent(yowLayerEvent)

    def broadcastEvent(self, yowLayerEvent):
        if not self.__stackInstances[-1].onEvent(yowLayerEvent):
            self.__stackInstances[-1].broadcastEvent(yowLayerEvent)

    def execDetached(self, fn):
        self.__class__.__detachedQueue.put(fn)

    def loop(self, *args, **kwargs):
        if "discrete" in kwargs:
            discreteVal = kwargs["discrete"]
            del kwargs["discrete"]
            while True:
                asyncore.loop(*args, **kwargs)
                time.sleep(discreteVal)
                try:
                    callback = self.__class__.__detachedQueue.get(False) #doesn't block
                    callback()
                except Queue.Empty:
                    pass
        else:
            asyncore.loop(*args, **kwargs)

    def _construct(self):
        logger.debug("Initializing stack")
        for s in self.__stack:
            if type(s) is tuple:
                logger.warn("Implicit declaration of parallel layers in a tuple is deprecated, pass a YowParallelLayer instead")
                inst = YowParallelLayer(s)
            else:
                if inspect.isclass(s):
                    if issubclass(s, YowLayer):
                        inst = s()
                    else:
                        raise ValueError("Stack must contain only subclasses of YowLayer")
                elif issubclass(s.__class__, YowLayer):
                        inst = s
                else:
                    raise ValueError("Stack must contain only subclasses of YowLayer")
                #inst = s()
            logger.debug("Constructed %s" % inst)
            inst.setStack(self)
            self.__stackInstances.append(inst)

        for i in range(0, len(self.__stackInstances)):
            upperLayer = self.__stackInstances[i + 1] if (i + 1) < len(self.__stackInstances) else None
            lowerLayer = self.__stackInstances[i - 1] if i > 0 else None
            self.__stackInstances[i].setLayers(upperLayer, lowerLayer)

    def getLayer(self, layerIndex):
        return self.__stackInstances[layerIndex]

