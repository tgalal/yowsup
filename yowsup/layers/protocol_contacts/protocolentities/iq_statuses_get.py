from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class GetStatusesIqProtocolEntity(IqProtocolEntity):
    XMLNS = "status"

    def __init__(self, jids, _id = None):
        """
        Request the statuses of users. Should be sent once after login.

        Args:
            - jids: A list of jids representing the users whose statuses you are
                trying to get.
        """
        super(GetStatusesIqProtocolEntity, self).__init__(self.__class__.XMLNS, _id, _type = "get", to = YowConstants.WHATSAPP_SERVER)
        self.setGetStatusesProps(jids)

    def setGetStatusesProps(self, jids):
        assert type(jids) is list, "jids must be a list of jids"
        self.jids = jids

    def __str__(self):
        out = super(GetStatusesIqProtocolEntity, self).__str__()
        out += "Numbers: %s\n" % (",".join(self.numbers))
        return out

    def toProtocolTreeNode(self):
        users = [ProtocolTreeNode("user", {'jid': jid}) for jid in self.jids]

        node = super(GetStatusesIqProtocolEntity, self).toProtocolTreeNode()
        statusNode = ProtocolTreeNode("status", None, users)
        node.addChild(statusNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GetStatusesIqProtocolEntity
        statusNode = node.getChild("status")
        userNodes = statusNode.getAllChildren()
        jids = [user['jid'] for user in userNodes]

        entity.setGetStatusesProps(jids)

        return entity
