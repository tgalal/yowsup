from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class GroupsResultIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" id="{{id}}" xmlns="w:g" from={{from_jid}}} to={{group_jid}}">
    </iq>
    '''
    def __init__(self, to = None, _from  = None, _id = None):
        super(GroupsResultIqProtocolEntity, self).__init__("w:g", _id, to = to, _from = _from)