from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class IqProtocolEntity(ProtocolEntity):
    schema = (__file__, "schemas/iq.xsd")
    '''
    <iq type="{{get | set}}" id="{{id}}" xmlns="{{xmlns}}" to="{{TO}}" from="{{FROM}}">
    </iq>
    '''

    TYPE_SET = "set"
    TYPE_GET = "get"
    TYPE_ERROR = "error"
    TYPE_RESULT = "result"

    TYPES = (TYPE_SET, TYPE_GET, TYPE_RESULT, TYPE_ERROR)
    def __init__(self, xmlns = None, _id = None, _type = None, to = None, _from = None):
        super(IqProtocolEntity, self).__init__("iq")

        assert _type in self.__class__.TYPES, "Iq of type %s is not implemented, can accept only (%s)" % (_type," | ".join(self.__class__.TYPES))
        assert not to or not _from, "Can't set from and to at the same time"
        self._id = self._generateId(True) if _id is None else _id
        self._from = _from
        self._type = _type
        self.xmlns = xmlns
        self.to = to

    def getId(self):
        return self._id

    def getType(self):
        return self._type

    def getXmlns(self):
        return self.xmlns

    def getFrom(self):
        return self._from

    def getTo(self):
        return self.to

    def getProtocolTreeNode(self, xmlns = None):
        attribs = {
            "id"          : self._id,
            "type"        : self._type
        }
        ns = None
        if xmlns is not None:
            # attribs["xmlns"] = xmlns
            ns = (None, xmlns)

        if self.to:
            attribs["to"] = self.to
        elif self._from:
            attribs["from"] = self._from

        return self._createProtocolTreeNode(attribs, None, data = None, ns = ns)

    def toProtocolTreeNode(self):
        return self.getProtocolTreeNode()

    def __str__(self):
        out  = "Iq:\n"
        out += "ID: %s\n" % self._id
        out += "Type: %s\n" % self._type
        if self.xmlns:
            out += "xmlns: %s\n" % self.xmlns
        if self.to:
            out += "to: %s\n" % self.to
        elif self._from:
            out += "from: %s\n" % self._from
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        return IqProtocolEntity(
            node.getAttributeValue("xmlns"),
            node.getAttributeValue("id"),
            node.getAttributeValue("type"),
            node.getAttributeValue("to"),
            node.getAttributeValue("from")
            )
