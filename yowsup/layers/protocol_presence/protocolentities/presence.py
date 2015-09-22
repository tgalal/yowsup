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

    def __init__(self, _type = None, name = None, _from = None, last = None):
        super(PresenceProtocolEntity, self).__init__("presence")
        self._type = _type
        self.name = name
        self._from = _from
        self.last = last

    def getType(self):
        return self._type

    def getName(self):
        return self.name

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]

    def getLast(self):
        return self.last

    def toProtocolTreeNode(self):
        attribs = {}
        if self._type:
            attribs["type"] = self._type
        if self.name:
            attribs["name"] = self.name
        if self._from:
            attribs["from"] = self._from
        if self.last:
            attribs["last"] = self.last

        return self._createProtocolTreeNode(attribs, None, None)

    def __str__(self):
        out  = "Presence:\n"
        if self._type:
            out += "Type: %s\n" % self._type
        if self.name:
            out += "Name: %s\n" % self.name
        if self._from:
            out += "From: %s\n" % self._from
        if self.last:
            out += "Last seen: %s\n" % self.last
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return PresenceProtocolEntity(
            node.getAttributeValue("type"),
            node.getAttributeValue("name"),
            node.getAttributeValue("from"),
            node.getAttributeValue("last")
            )

