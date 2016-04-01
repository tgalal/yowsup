from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .receipt import ReceiptProtocolEntity
from yowsup.layers.protocol_acks.protocolentities  import OutgoingAckProtocolEntity

class IncomingReceiptProtocolEntity(ReceiptProtocolEntity):

    '''
    delivered:
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15"></receipt>

    read
    <receipt to="xxxxxxxxxxx@s.whatsapp.net" id="1415389947-15" type="read"></receipt>

    delivered to participant in group:
    <receipt participant="xxxxxxxxxx@s.whatsapp.net" from="yyyyyyyyyyyyy@g.us" id="1431204051-9" t="1431204094"></receipt>

    read by participant in group:
    <receipt participant="xxxxxxxxxx@s.whatsapp.net" t="1431204235" from="yyyyyyyyyyyyy@g.us" id="1431204051-9" type="read"></receipt>

    multiple items:
    <receipt type="read" from="xxxxxxxxxxxx@s.whatsapp.net" id="1431364583-191" t="1431365553">
        <list>
            <item id="1431364572-189"></item>
            <item id="1431364575-190"></item>
        </list>
    </receipt>

    multiple items to group:
    <receipt participant="xxxxxxxxxxxx@s.whatsapp.net" t="1431330533" from="yyyyyyyyyyyyyy@g.us" id="1431330385-323" type="read">
        <list>
            <item id="1431330096-317"></item>
            <item id="1431330373-320"></item>
            <item id="1431330373-321"></item>
            <item id="1431330385-322"></item>
        </list>
    </receipt>

    INCOMING
    <receipt offline="0" from="xxxxxxxxxx@s.whatsapp.net" id="1415577964-1" t="1415578027"></receipt>
    '''

    def __init__(self, _id, _from, timestamp, offline = None, type = None, participant = None, items = None):
        super(IncomingReceiptProtocolEntity, self).__init__(_id)
        self.setIncomingData(_from, timestamp, offline, type, participant, items)

    def getType(self):
        return self.type

    def getParticipant(self):
        return self.participant

    def getFrom(self, full = True):
        return self._from if full else self._from.split('@')[0]

    def setIncomingData(self, _from, timestamp, offline, type = None, participant = None, items = None):
        self._from = _from
        self.timestamp = timestamp
        self.type = type
        self.participant = participant
        if offline is not None:
            self.offline = True if offline == "1" else False
        else:
            self.offline = None
        self.items = items

    def toProtocolTreeNode(self):
        node = super(IncomingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("from", self._from)
        node.setAttribute("t", str(self.timestamp))
        if self.offline is not None:
            node.setAttribute("offline", "1" if self.offline else "0")
        if self.type is not None:
            node.setAttribute("type", self.type)
        if self.participant is not None:
            node.setAttribute("participant", self.participant)

        if self.items is not None:
            inodes = []
            for item in self.items:
                inode = ProtocolTreeNode("item", {"id": item})
                inodes.append(inode)

            lnode = ProtocolTreeNode("list")
            lnode.addChildren(inodes)
            node.addChild(lnode)
        return node

    def __str__(self):
        out = super(IncomingReceiptProtocolEntity, self).__str__()
        out += "From: %s\n" % self._from
        out += "Timestamp: %s\n" % self.timestamp
        if self.offline is not None:
            out += "Offline: %s\n" % ("1" if self.offline else "0")
        if self.type is not None:
            out += "Type: %s\n" % (self.type)
        if self.participant is not None:
            out += "Participant: %s\n" % (self.participant)
        if self.items is not None:
            out += "Items: %s\n" % " ".join(self.items)
        return out

    def ack(self):
        return OutgoingAckProtocolEntity(self.getId(), "receipt", self.getType(), self.getFrom(), participant = self.participant)

    @staticmethod
    def fromProtocolTreeNode(node):
        items = None
        listNode = node.getChild("list")
        if listNode is not None:
            items = []
            for inode in listNode.getAllChildren("item"):
               items.append(inode["id"])
        return IncomingReceiptProtocolEntity(
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("offline"),
            node.getAttributeValue("type"),
            node.getAttributeValue("participant"),
            items
            )
