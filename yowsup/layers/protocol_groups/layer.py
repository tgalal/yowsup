from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowGroupsProtocolLayer(YowProtocolLayer):

    HANDLE = (
        CreateGroupsIqProtocolEntity,
        DeleteGroupsIqProtocolEntity,
        InfoGroupsIqProtocolEntity,
        LeaveGroupsIqProtocolEntity,
        ListGroupsIqProtocolEntity,
        ParticipantsGroupsIqProtocolEntity
        #AddPariticipantsIqProtocolEntity,
        #RemoveParticipantsIqProtocolEntity
    )

    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq),
            "notification": (self.recvNotification, None)
        }
        super(YowGroupsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Groups Iq Layer"

    def sendIq(self, entity):
        if entity.__class__ in self.__class__.HANDLE:
            self.entityToLower(entity)

    def recvIq(self, node):
        if node["type"] == "result" and node["from"] == "g.us" and len(node.getAllChildren()):
            self.toUpper(ListGroupsResultIqProtocolEntity.fromProtocolTreeNode(node))
        elif node["type"] == "result" and len(node.getAllChildren()):
            self.toUpper(ListParticipantsResultIqProtocolEntity.fromProtocolTreeNode(node))

    def recvNotification(self, node):
        if node["type"] == "subject":
            self.toUpper(SubjectNotificationProtocolEntity.fromProtocolTreeNode(node))