from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity

'''
<iq type="result" from="{{JID}}@s.whatsapp.net" id="{{IQ:ID}}">
<privacy>
<category name="last" value="all">
</category>
<category name="status" value="all">
</category>
<category name="profile" value="all">
</category>
</privacy>
</iq>
'''

class ResultPrivacyIqProtocolEntity(ResultIqProtocolEntity):
    NODE_PRIVACY="privacy"

    def __init__(self, privacy):
        super(ResultPrivacyIqProtocolEntity, self).__init__()
        self.setProps(privacy)

    def setProps(self, privacy):
        assert type(privacy) is dict, "Privacy must be a dict {name => value}"
        self.privacy = privacy

    def __str__(self):
        out = super(ResultPrivacyIqProtocolEntity, self).__str__()
        out += "Privacy settings\n"
        for name, value in self.privacy.items():
            out += "Category %s  --> %s\n" % (name, value)
        return out

    def toProtocolTreeNode(self):
        node = super(ResultPrivacyIqProtocolEntity, self).toProtocolTreeNode()
        queryNode = ProtocolTreeNode(self.__class__.NODE_PRIVACY)
        node.addChild(queryNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(ResultPrivacyIqProtocolEntity, ResultPrivacyIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = ResultPrivacyIqProtocolEntity
        privacyNode = node.getChild(ResultPrivacyIqProtocolEntity.NODE_PRIVACY)
        privacy = {}
        for categoryNode in privacyNode.getAllChildren():
            privacy[categoryNode["name"]] = categoryNode["value"]
        entity.setProps(privacy)
        return entity
