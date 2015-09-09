from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ib import IbProtocolEntity
class AccountIbProtocolEntity(IbProtocolEntity):
    '''
    <ib from="s.whatsapp.net">
        <account status="active | ?" kind="paid" creation="timestamp" expiration="timestamp"></account>
    </ib>
    '''

    STATUS_ACTIVE = "active"
    KIND_PAD      = "paid"

    def __init__(self, status, kind, creation, expiration):
        super(AccountIbProtocolEntity, self).__init__()
        self.setProps(status, kind, creation, expiration)


    def setProps(self, status, kind, creation, expiration):
        self.status = status
        self.creation = int(creation)
        self.kind = kind
        self.expiration= int(expiration)

    def toProtocolTreeNode(self):
        node = super(AccountIbProtocolEntity, self).toProtocolTreeNode()
        accountChild = ProtocolTreeNode("account",
                                        {
                                            "status": self.status,
                                            "kind": self.kind,
                                            "creation": int(self.creation),
                                            "expiration": int(self.expiration)

                                        })
        node.addChild(accountChild)
        return node

    def __str__(self):
        out = super(AccountIbProtocolEntity, self).__str__()
        out += "Status: %s\n" % self.status
        out += "Kind: %s\n" % self.kind
        out += "Creation: %s\n" % self.creation
        out += "Expiration: %s\n" % self.expiration

        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IbProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AccountIbProtocolEntity
        accountNode = node.getChild("account")
        entity.setProps(
            accountNode["status"],
            accountNode["kind"],
            accountNode["creation"],
            accountNode["expiration"]
        )