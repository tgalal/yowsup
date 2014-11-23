from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class GroupsIqProtocolEntity(IqProtocolEntity):
    '''
    <iq type="{{get | set?}}" id="{{id}}" xmlns="w:g", to={{group_jid}}">
    </iq>
    '''
    def __init__(self, to = None, _from  = None, _id = None, _type = None):
        super(GroupsIqProtocolEntity, self).__init__("w:g", _id, _type, to = to, _from = _from)