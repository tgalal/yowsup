from yowsup.structs import  ProtocolTreeNode
from .iq import IqProtocolEntity
class ErrorIqProtocolEntity(IqProtocolEntity):

    '''<iq id="1417113419-0" from="{{jid}}" type="error">
    <error text="not-acceptable" code="406" backoff="3600">
    </error>
    </iq>
    '''

    def __init__(self, _id, _from, code, text, backoff= 0 ):
        super(ErrorIqProtocolEntity, self).__init__(xmlns = None, _id = _id, _type = "error", _from = _from)
        self.setErrorProps(code, text, backoff)

    def setErrorProps(self, code, text, backoff):
        self.code = int(code)
        self.text = text
        self.backoff = int(backoff) if backoff else 0

    def toProtocolTreeNode(self):
        node = super(ErrorIqProtocolEntity, self).toProtocolTreeNode()
        errorNode = ProtocolTreeNode("error", {"text": self.text, "code": str(self.code)})
        if self.backoff:
            errorNode.setAttribute("backoff", str(self.backoff))
        node.addChild(errorNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ErrorIqProtocolEntity
        errorNode = node.getChild("error")
        entity.setErrorProps(errorNode.getAttributeValue("code"),
                             errorNode.getAttributeValue("text"),
                             errorNode.getAttributeValue("backoff"))
        return entity


