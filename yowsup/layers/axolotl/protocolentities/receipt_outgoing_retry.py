from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.axolotl.protocolentities.iq_keys_get_result import ResultGetKeysIqProtocolEntity
class RetryOutgoingReceiptProtocolEntity(OutgoingReceiptProtocolEntity):

    '''
    <receipt type="retry" to="xxxxxxxxxxx@s.whatsapp.net" participant="" id="1415389947-12" t="1432833777">
        <retry count="1" t="1432833266" id="1415389947-12" v="1">
        </retry>
        <registration>
            HEX:xxxxxxxxx
        </registration>
    </receipt>
    '''

    def __init__(self, _id, jid, localRegistrationId, retryTimestamp, v = 1, count = 1, participant = None):
        super(RetryOutgoingReceiptProtocolEntity, self).__init__(_id, jid, participant=participant)
        '''
            Note to self: Android clients won't retry sending if the retry node didn't contain the message timestamp
        '''
        self.setRetryData(localRegistrationId, v,count, retryTimestamp)

    def setRetryData(self, localRegistrationId, v, count, retryTimestamp):
        self.localRegistrationId =  localRegistrationId
        self.v = v
        self.count = count
        self.retryTimestamp = int(retryTimestamp)

    def toProtocolTreeNode(self):
        node = super(RetryOutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("type", "retry")

        retryAttribs = {
            "count": str(self.count),
            "id":self.getId(),
            "v":str(self.v),
            "t":  str(self.retryTimestamp)
        }

        retry = ProtocolTreeNode("retry", retryAttribs)
        node.addChild(retry)
        registration = ProtocolTreeNode("registration", data=ResultGetKeysIqProtocolEntity._intToBytes(self.localRegistrationId))
        node.addChild(registration)
        return node

    def __str__(self):
        out = super(RetryOutgoingReceiptProtocolEntity, self).__str__()
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = OutgoingReceiptProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RetryOutgoingReceiptProtocolEntity
        retryNode = node.getChild("retry")
        entity.setRetryData(ResultGetKeysIqProtocolEntity._bytesToInt(node.getChild("registration").data), retryNode["v"], retryNode["count"], retryNode["t"])

        return entity

    @staticmethod
    def fromMessageNode(messageNodeToBeRetried, localRegistrationId):
        return RetryOutgoingReceiptProtocolEntity(
            messageNodeToBeRetried.getAttributeValue("id"),
            messageNodeToBeRetried.getAttributeValue("from"),
            localRegistrationId,
            messageNodeToBeRetried.getAttributeValue("t"),
            participant=messageNodeToBeRetried.getAttributeValue("participant")
        )
