from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowGroupsProtocolLayer(YowProtocolLayer):

    HANDLE = (
        CreateGroupsIqProtocolEntity,
        DeleteGroupsIqProtocolEntity,
        InfoGroupsIqProtocolEntity,
        LeaveGroupsIqProtocolEntity,
        ListGroupsIqProtocolEntity,
        #AddPariticipantsIqProtocolEntity,
        #RemoveParticipantsIqProtocolEntity
    )

    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowGroupsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Groups Iq Layer"

    def sendIq(self, entity):
        if entity.__class__ in self.__class__.HANDLE:
            self.entityToLower(entity)

    def recvIq(self, node):
        return

