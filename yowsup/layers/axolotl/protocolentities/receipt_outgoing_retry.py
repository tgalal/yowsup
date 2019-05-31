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

    def __init__(self, _id, jid, local_registration_id, retry_timestamp, v=1, count=1, participant=None):
        super(RetryOutgoingReceiptProtocolEntity, self).__init__(_id, jid, participant=participant)
        '''
            Note to self: Android clients won't retry sending if the retry node didn't contain the message timestamp
        '''
        self.local_registration_id = local_registration_id
        self.v = v
        self.retry_timestamp = retry_timestamp
        self.count = count

    @property
    def local_registration_id(self):
        return self._local_registration_id

    @local_registration_id.setter
    def local_registration_id(self, value):
        self._local_registration_id = value

    @property
    def v(self):
        return self._v

    @v.setter
    def v(self, value):
        self._v = value

    @property
    def retry_timestamp(self):
        return self._retry_timestamp

    @retry_timestamp.setter
    def retry_timestamp(self, value):
        self._retry_timestamp = value

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def toProtocolTreeNode(self):
        node = super(RetryOutgoingReceiptProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("type", "retry")

        retry_attrs = {
            "count": str(self.count),
            "id":self.getId(),
            "v":str(self.v),
            "t":  str(self.retry_timestamp)
        }

        retry = ProtocolTreeNode("retry", retry_attrs)
        node.addChild(retry)
        registration = ProtocolTreeNode(
            "registration",
            data=ResultGetKeysIqProtocolEntity._intToBytes(self.local_registration_id)
        )
        node.addChild(registration)
        return node

    def __str__(self):
        out = super(RetryOutgoingReceiptProtocolEntity, self).__str__()
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = OutgoingReceiptProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RetryOutgoingReceiptProtocolEntity
        retry_node = node.getChild("retry")
        entity.setRetryData(
            ResultGetKeysIqProtocolEntity._bytesToInt(
                node.getChild("registration").data
            ),
            retry_node["v"], retry_node["count"], retry_node["t"]
        )

        return entity

    @staticmethod
    def fromMessageNode(message_node, local_registration_id):
        return RetryOutgoingReceiptProtocolEntity(
            message_node.getAttributeValue("id"),
            message_node.getAttributeValue("from"),
            local_registration_id,
            message_node.getAttributeValue("t"),
            participant=message_node.getAttributeValue("participant")
        )
