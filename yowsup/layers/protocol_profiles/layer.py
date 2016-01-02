from yowsup.layers import  YowProtocolLayer
from .protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity, ResultIqProtocolEntity
class YowProfilesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowProfilesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Profiles Layer"

    def sendIq(self, entity):
        if entity.getXmlns() == "w:profile:picture":
            if entity.getType() == "get":
                self._sendIq(entity, self.onGetPictureResult, self.onGetPictureError)
            elif entity.getType() == "set":
                self._sendIq(entity, self.onSetPictureResult, self.onSetPictureError)
            elif entity.getType() == "delete":
                self._sendIq(entity, self.onDeletePictureResult, self.onDeletePictureError)
        elif entity.getXmlns() == "status":
            self._sendIq(entity, self.onSetStatusResult, self.onSetStatusError)
        elif entity.getXmlns() == "privacy":
            self._sendIq(entity, self.onPrivacyResult, self.onPrivacyError)

    def recvIq(self, node):
        pass

    def onPrivacyResult(self, resultNode, originIqRequestEntity):
        self.toUpper(ResultPrivacyIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onPrivacyError(self, errorNode, originalIqRequestEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))

    def onSetStatusResult(self, resultNode, originIqRequestEntity):
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onSetStatusError(self, errorNode, originalIqRequestEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))

    def onGetPictureResult(self, resultNode, originalIqRequestEntity):
        self.toUpper(ResultGetPictureIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onGetPictureError(self, errorNode, originalIqRequestEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))

    def onSetPictureResult(self, resultNode, originalIqRequestEntity):
        self.toUpper(ResultGetPictureIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onSetPictureError(self, errorNode, originalIqRequestEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))

    def onDeletePictureResult(self, resultNode, originalIqRequestEntity):
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onDeletePictureError(self, errorNode, originalIqRequestEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))
