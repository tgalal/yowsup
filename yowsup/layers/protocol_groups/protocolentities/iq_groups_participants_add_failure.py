from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
class FailureAddParticipantsIqProtocolEntity(ErrorIqProtocolEntity):
    '''
    <iq type="error" from="{{group_jid}}" id="{{id}}">
        <error text="item-not-found" code="404">
        </error>
    </iq>
    '''

    def __init__(self, _id, _from, _code, _text, _backoff= 0 ):
        super(FailureAddParticipantsIqProtocolEntity, self).__init__(_from = _from,
                                                                     _id = _id, code = _code,
                                                                     text = _text, backoff = _backoff)
    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ErrorIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = FailureAddParticipantsIqProtocolEntity
        return entity