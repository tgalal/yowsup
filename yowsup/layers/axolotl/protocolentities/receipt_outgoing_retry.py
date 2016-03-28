from yowsup.structs import ProtocolEntity, ProtocolTreeNode
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

    def __init__(self, _id, to, t, v = "1", count = "1",regData = "", participant = None):
        super(RetryOutgoingReceiptProtocolEntity, self).__init__(_id,to, participant=participant)
        self.setRetryData(t,v,count,regData)

    def setRetryData(self, t,v,count,regData):
        self.t = int(t)
        self.v = int(v)
        self.count = int(count)
        self.regData = regData

    def setRegData(self,regData):
        '''
        In axolotl layer:
        regData = self.store.getLocalRegistrationId()
        '''
        self.regData = ResultGetKeysIqProtocolEntity._intToBytes(regData)

    def toProtocolTreeNode(self):
        node = super(RetryOutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("type", "retry")
        retry = ProtocolTreeNode("retry", {"count": str(self.count),"t":str(self.t),"id":self.getId(),"v":str(self.v)})
        node.addChild(retry)
        registration = ProtocolTreeNode("registration",data=self.regData)
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
        entity.setRetryData(retryNode["t"], retryNode["v"], retryNode["count"], node.getChild("registration").data)


    @staticmethod
    def fromMessageNode(MessageNodeToBeRetried, desiredEncryptionVersion = "1"):
        return RetryOutgoingReceiptProtocolEntity(
            MessageNodeToBeRetried.getAttributeValue("id"),
            MessageNodeToBeRetried.getAttributeValue("from"),
            MessageNodeToBeRetried.getAttributeValue("t"),
            desiredEncryptionVersion,
            participant=MessageNodeToBeRetried.getAttributeValue("participant")
        )
