from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode


class GetKeysIqProtocolEntity(IqProtocolEntity):
    def __init__(self, jids, reason=None):
        super(GetKeysIqProtocolEntity, self).__init__("encrypt", _type="get", to=YowConstants.WHATSAPP_SERVER)
        self.jids = jids
        self.reason = reason

    @property
    def reason(self):
        # type: () -> str
        return self._reason

    @reason.setter
    def reason(self, value):
        # type: (str) -> None
        self._reason = value

    @property
    def jids(self):
        # type: () -> list[str]
        return self._jids

    @jids.setter
    def jids(self, value):
        # type: (list[str]) -> None
        assert type(value) is list, "expected list of jids, got %s" % type(value)
        self._jids = value

    def toProtocolTreeNode(self):
        node = super(GetKeysIqProtocolEntity, self).toProtocolTreeNode()
        keyNode = ProtocolTreeNode("key")

        for jid in self.jids:
            attrs = { "jid": jid }
            if self.reason is not None:
                attrs["reason"] = self.reason
            userNode = ProtocolTreeNode("user", attrs)
            keyNode.addChild(userNode)
        node.addChild(keyNode)
        return node
