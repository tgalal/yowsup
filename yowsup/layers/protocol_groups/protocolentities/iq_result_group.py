from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class GroupResultIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" id="{{id}}" xmlns="w:g" from="{{from_jid}}}" to="{{group_jid}}">
    </iq>

    TODO: It seems that this class is useless now as it works without the xmlns too,
          but that needs to be confirmed.
    '''
    def __init__(self, _id = None, _from  = None):
        super(GroupsResultIqProtocolEntity, self).__init__("w:g", _id, _from = _from)