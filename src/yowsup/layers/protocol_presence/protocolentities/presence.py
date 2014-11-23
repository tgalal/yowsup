from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class PresenceProtocolEntity(ProtocolEntity):
    '''
    <presence type="{{type}} name={{push_name}}"></presence>
    Should normally be either type or name

    when contact goes offline:
    <presence type="unavailable" from="{{contact_jid}}" last="deny | ?">
    </presence>

    when contact goes online:
    <presence from="contact_jid">
    </presence>

    '''

    def __init__(self, _type = None, name = None):
        super(PresenceProtocolEntity, self).__init__("presence")
        self._type= _type
        self.name = name

    def getType(self):
        return _type

    def getName(self):
        return self.name
    
    def toProtocolTreeNode(self):
        attribs = {}
        if self._type:
            attribs["type"] = self._type

        if self.name:
            attribs["name"] = self.name


        return self._createProtocolTreeNode(attribs, None, None)

    def __str__(self):
        out  = "Presence:\n"
        if self._type:
            out += "Type: %s\n" % self._type

        if self.name:
            out += "Name: %s\n" % self.name
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return PresenceProtocolEntity(
            node.getAttributeValue("type"),
            node.getAttributeValue("name")
            )

