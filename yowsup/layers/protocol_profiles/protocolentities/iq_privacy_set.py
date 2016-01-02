from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode

'''
<iq xmlns="privacy" type="set" id="{{IQ_ID}}">
<privacy>
<category name="status" value="none">
<category name="profile" value="none">
<category name="last" value="none">
</category>
</privacy>
</iq>
'''

class SetPrivacyIqProtocolEntity(IqProtocolEntity):
    NAMES = ["status", "profile", "last"]
    VALUES = ["all", "contacts", "none"]
    XMLNS = "privacy"

    def __init__(self, value="all", names = None):
        # names can be a string with some element in VALUES or an array with strings with elements in VALUES
        # by default, all names are used
        super(SetPrivacyIqProtocolEntity, self).__init__(self.__class__.XMLNS, _type="set")
        self.setNames(names)
        self.setValue(value)

    @staticmethod
    def checkValidNames(names):
        names = names if names else SetPrivacyIqProtocolEntity.NAMES
        if not type(names) is list:
            names = [names]

        for name in names:
            if not name in SetPrivacyIqProtocolEntity.NAMES:
                raise Exception("Name should be in: '" + "', '".join(SetPrivacyIqProtocolEntity.NAMES) + "' but is '" + name + "'")
        return names

    @staticmethod
    def checkValidValue(value):
        if not value in SetPrivacyIqProtocolEntity.VALUES:
            raise Exception("Value should be in: '" + "', '".join(SetPrivacyIqProtocolEntity.VALUES) + "' but is '" + value + "'")
        return value

    def setNames(self, names):
        self.names = SetPrivacyIqProtocolEntity.checkValidNames(names)

    def setValue(self, value):
        self.value = SetPrivacyIqProtocolEntity.checkValidValue(value)

    def toProtocolTreeNode(self):
        node = super(SetPrivacyIqProtocolEntity, self).toProtocolTreeNode()
        queryNode = ProtocolTreeNode(self.__class__.XMLNS)
        for name in self.names:
            listNode = ProtocolTreeNode("category", {"name": name, "value": self.value})
            queryNode.addChild(listNode)
        node.addChild(queryNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SetPrivacyIqProtocolEntity
        privacyNode = node.getChild(SetPrivacyIqProtocolEntity.XMLNS)
        names = [] 
        for categoryNode in privacyNode.getAllChildren():
            names.append(categoryNode["name"])
        entity.setNames(names)
        entity.setValue("all")
        return entity
