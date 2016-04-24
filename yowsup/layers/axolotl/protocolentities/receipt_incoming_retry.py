from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_receipts.protocolentities import IncomingReceiptProtocolEntity
from yowsup.layers.axolotl.protocolentities.iq_keys_get_result import ResultGetKeysIqProtocolEntity
class RetryIncomingReceiptProtocolEntity(IncomingReceiptProtocolEntity):

    '''
    <receipt type="retry" from="xxxxxxxxxxx@s.whatsapp.net" participant="" id="1415389947-12" t="1432833777">
        <retry count="1" t="1432833266" id="1415389947-12" v="1">
        </retry>
        <registration>
            HEX:xxxxxxxxx
        </registration>
    </receipt>
    '''

    def __init__(self, _id, jid, remoteRegistrationId, receiptTimestamp, retryTimestamp, v = 1, count = 1, participant = None, offline = None):
        super(RetryIncomingReceiptProtocolEntity, self).__init__(_id, jid, receiptTimestamp, offline=offline, type="retry", participant=participant)
        self.setRetryData(remoteRegistrationId, v,count, retryTimestamp)

    def setRetryData(self, remoteRegistrationId, v, count, retryTimestamp):
        self.remoteRegistrationId =  remoteRegistrationId
        self.v = int(v)
        self.count = int(count)
        self.retryTimestamp = int(retryTimestamp)

    def toProtocolTreeNode(self):
        node = super(RetryIncomingReceiptProtocolEntity, self).toProtocolTreeNode()

        retry = ProtocolTreeNode("retry", {
            "count": str(self.count),
            "id": self.getId(),
            "v": str(self.v),
            "t": str(self.retryTimestamp)
        })
        node.addChild(retry)
        registration = ProtocolTreeNode("registration", data=ResultGetKeysIqProtocolEntity._intToBytes(self.remoteRegistrationId))
        node.addChild(registration)
        return node

    def getRetryCount(self):
        return self.count

    def getRetryJid(self):
        return self.getParticipant() or self.getFrom()

    def __str__(self):
        out = super(RetryIncomingReceiptProtocolEntity, self).__str__()
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IncomingReceiptProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RetryIncomingReceiptProtocolEntity
        retryNode = node.getChild("retry")
        entity.setRetryData(ResultGetKeysIqProtocolEntity._bytesToInt(node.getChild("registration").data), retryNode["v"], retryNode["count"], retryNode["t"])

        return entity
