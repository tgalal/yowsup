from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
import logging
logger = logging.getLogger(__name__)


class YowGroupsProtocolLayer(YowProtocolLayer):

    HANDLE = (
        CreateGroupsIqProtocolEntity,
        DeleteGroupsIqProtocolEntity,
        InfoGroupsIqProtocolEntity,
        LeaveGroupsIqProtocolEntity,
        ListGroupsIqProtocolEntity,
        SubjectGroupsIqProtocolEntity,
        ParticipantsGroupsIqProtocolEntity,
        AddParticipantsIqProtocolEntity,
        RemoveParticipantsIqProtocolEntity
    )

    def __init__(self):
        handleMap = {
            "iq": (None, self.sendIq),
            "notification": (self.recvNotification, None)
        }
        super(YowGroupsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Groups Iq Layer"

    def sendIq(self, entity):
        if entity.__class__ in self.__class__.HANDLE:
            if entity.__class__ == SubjectGroupsIqProtocolEntity:
                self._sendIq(entity, self.onSetSubjectSuccess, self.onSetSubjectFailed)
            elif entity.__class__ == CreateGroupsIqProtocolEntity:
                self._sendIq(entity, self.onCreateGroupSuccess, self.onCreateGroupFailed)
            elif entity.__class__ == ParticipantsGroupsIqProtocolEntity:
                self._sendIq(entity, self.onGetParticipantsResult)
            elif entity.__class__ == AddParticipantsIqProtocolEntity:
                self._sendIq(entity, self.onAddParticipantsSuccess, self.onAddParticipantsFailed)
            elif entity.__class__ == RemoveParticipantsIqProtocolEntity:
                self._sendIq(entity, self.onRemoveParticipantsSuccess, self.onRemoveParticipantsFailed)
            elif entity.__class__ == ListGroupsIqProtocolEntity:
                self._sendIq(entity, self.onListGroupsResult)
            elif entity.__class__ == LeaveGroupsIqProtocolEntity:
                self._sendIq(entity, self.onLeaveGroupSuccess, self.onLeaveGroupFailed)
            elif entity.__class__ == InfoGroupsIqProtocolEntity:
                self._sendIq(entity, self.onInfoGroupSuccess, self.onInfoGroupFailed)
            else:
                self.entityToLower(entity)

    def onCreateGroupSuccess(self, node, originalIqEntity):
        logger.info("Group create success")
        self.toUpper(SuccessCreateGroupsIqProtocolEntity.fromProtocolTreeNode(node))

    def onCreateGroupFailed(self, node, originalIqEntity):
        logger.error("Group create failed")

    def onSetSubjectSuccess(self, node, originalIqEntity):
        logger.info("Group subject change success")

    def onSetSubjectFailed(self, node, originalIqEntity):
        logger.error("Group subject change failed")

    def onGetParticipantsResult(self, node, originalIqEntity):
        self.toUpper(ListParticipantsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onAddParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group add participants success")
        self.toUpper(SuccessAddParticipantsIqProtocolEntity.fromProtocolTreeNode(node))

    def onRemoveParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group remove participants failed")

    def onRemoveParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group remove participants success")
        self.toUpper(SuccessRemoveParticipantsIqProtocolEntity.fromProtocolTreeNode(node))

    def onAddParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group add participants failed")

    def onListGroupsResult(self, node, originalIqEntity):
        self.toUpper(ListGroupsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onLeaveGroupSuccess(self, node, originalIqEntity):
        logger.info("Group leave success")
        self.toUpper(SuccessLeaveGroupsIqProtocolEntity.fromProtocolTreeNode(node))

    def onLeaveGroupFailed(self, node, originalIqEntity):
        logger.error("Group leave failed")

    def onInfoGroupSuccess(self, node, originalIqEntity):
        logger.info("Group info success")
        self.toUpper(InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onInfoGroupFailed(self, node, originalIqEntity):
        logger.error("Group info failed")

    def recvNotification(self, node):
        if node["type"] == "w:gp2":
            if node.getChild("subject"):
                self.toUpper(SubjectGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("create"):
                self.toUpper(CreateGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
