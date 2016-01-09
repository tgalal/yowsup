import time
import logging
from threading import Thread, Lock
from yowsup.layers import YowProtocolLayer, YowLayerEvent, EventCallback
from yowsup.common import YowConstants
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.auth import YowAuthenticationProtocolLayer
from .protocolentities import *


class YowIqProtocolLayer(YowProtocolLayer):
    
    PROP_PING_INTERVAL               = "org.openwhatsapp.yowsup.prop.pinginterval"
    
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        self._pingThread = None
        self._pingQueue = {}
        self._pingQueueLock = Lock()
        self.__logger = logging.getLogger(__name__)
        super(YowIqProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Iq Layer"

    def onPong(self, protocolTreeNode, pingEntity):
        self.gotPong(pingEntity.getId())
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(protocolTreeNode))

    def sendIq(self, entity):
        if entity.getXmlns() == "w:p":
            self._sendIq(entity, self.onPong)
        elif entity.getXmlns() in ("urn:xmpp:whatsapp:push", "w", "urn:xmpp:whatsapp:account", "encrypt"):
            self.toLower(entity.toProtocolTreeNode())

    def recvIq(self, node):
        if node["xmlns"] == "urn:xmpp:ping":
            entity = PongResultIqProtocolEntity(YowConstants.DOMAIN, node["id"])
            self.toLower(entity.toProtocolTreeNode())

    def gotPong(self, pingId):
        self._pingQueueLock.acquire()
        if pingId in self._pingQueue:
            self._pingQueue = {}
        self._pingQueueLock.release()

    def waitPong(self, id):
        self._pingQueueLock.acquire()
        self._pingQueue[id] = None
        pingQueueSize = len(self._pingQueue)
        self._pingQueueLock.release()
        self.__logger.debug("ping queue size: %d" % pingQueueSize)
        if pingQueueSize >= 2:
            self.getStack().broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT, reason = "Ping Timeout"))

    @EventCallback(YowAuthenticationProtocolLayer.EVENT_AUTHED)
    def onAuthed(self, event):
        interval = self.getProp(self.__class__.PROP_PING_INTERVAL, 50)
        if not self._pingThread and interval > 0:
            self._pingQueue = {}
            self._pingThread = YowPingThread(self, interval)
            self.__logger.debug("starting ping thread.")
            self._pingThread.start()
    
    
    def stop_thread(self):
        if self._pingThread:
            self.__logger.debug("stopping ping thread")
            if self._pingThread:
                self._pingThread.stop()
                self._pingThread = None
            self._pingQueue = {}
        
    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECT)
    def onDisconnect(self, event):
        self.stop_thread()
    
    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onDisconnected(self, event):
        self.stop_thread()
            
class YowPingThread(Thread):
    def __init__(self, layer, interval):
        assert type(layer) is YowIqProtocolLayer, "layer must be a YowIqProtocolLayer, got %s instead." % type(layer)
        self._layer = layer
        self._interval = interval
        self._stop = False
        self.__logger = logging.getLogger(__name__)
        super(YowPingThread, self).__init__()
        self.daemon = True
        self.name = "YowPing%s" % self.name

    def run(self):
        while not self._stop:
            for i in range(0, self._interval):
                time.sleep(1)
                if self._stop:
                    self.__logger.debug("%s - ping thread stopped" % self.name)
                    return
            ping = PingIqProtocolEntity()
            self._layer.waitPong(ping.getId())
            if not self._stop:
                self._layer.sendIq(ping)

    def stop(self):
        self._stop = True
