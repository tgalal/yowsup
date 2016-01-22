from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
from yowsup.layers.protocol_iq.protocolentities.iq_result import ResultIqProtocolEntity
from .protocolentities import *
import logging
logger = logging.getLogger(__name__)


class YowGroupsProtocolLayer(YowProtocolLayer):

    HANDLE = (
        CreateGroupsIqProtocolEntity,
        InfoGroupsIqProtocolEntity,
        LeaveGroupsIqProtocolEntity,
        ListGroupsIqProtocolEntity,
        SubjectGroupsIqProtocolEntity,
        ParticipantsGroupsIqProtocolEntity,
        AddParticipantsIqProtocolEntity,
        PromoteParticipantsIqProtocolEntity,
        DemoteParticipantsIqProtocolEntity,
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
            elif entity.__class__ == PromoteParticipantsIqProtocolEntity:
                self._sendIq(entity, self.onPromoteParticipantsSuccess, self.onPromoteParticipantsFailed)
            elif entity.__class__ == DemoteParticipantsIqProtocolEntity:
                self._sendIq(entity, self.onDemoteParticipantsSuccess, self.onDemoteParticipantsFailed)
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
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onSetSubjectSuccess(self, node, originalIqEntity):
        logger.info("Group subject change success")
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onSetSubjectFailed(self, node, originalIqEntity):
        logger.error("Group subject change failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onGetParticipantsResult(self, node, originalIqEntity):
        self.toUpper(ListParticipantsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onAddParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group add participants success")
        self.toUpper(SuccessAddParticipantsIqProtocolEntity.fromProtocolTreeNode(node))

    def onRemoveParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group remove participants failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onRemoveParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group remove participants success")
        self.toUpper(SuccessRemoveParticipantsIqProtocolEntity.fromProtocolTreeNode(node))

    def onPromoteParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group promote participants failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onPromoteParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group promote participants success")
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onDemoteParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group demote participants failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onDemoteParticipantsSuccess(self, node, originalIqEntity):
        logger.info("Group demote participants success")
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onAddParticipantsFailed(self, node, originalIqEntity):
        logger.error("Group add participants failed")
        self.toUpper(FailureAddParticipantsIqProtocolEntity.fromProtocolTreeNode(node))

    def onListGroupsResult(self, node, originalIqEntity):
        self.toUpper(ListGroupsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onLeaveGroupSuccess(self, node, originalIqEntity):
        logger.info("Group leave success")
        self.toUpper(SuccessLeaveGroupsIqProtocolEntity.fromProtocolTreeNode(node))

    def onLeaveGroupFailed(self, node, originalIqEntity):
        logger.error("Group leave failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def onInfoGroupSuccess(self, node, originalIqEntity):
        logger.info("Group info success")
        self.toUpper(InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def onInfoGroupFailed(self, node, originalIqEntity):
        logger.error("Group info failed")
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))

    def recvNotification(self, node):
        if node["type"] == "w:gp2":
            if node.getChild("subject"):
                self.toUpper(SubjectGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("create"):
                self.toUpper(CreateGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("remove"):
                self.toUpper(RemoveGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("add"):
                self.toUpper(AddGroupsNotificationProtocolEntity.fromProtocolTreeNode(node))
