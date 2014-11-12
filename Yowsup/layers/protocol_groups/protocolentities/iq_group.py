from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from Yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class GroupIqProtocolEntity(IqProtocolEntity):
    '''
    <iq type="{{get | set?}}" id="{{id}}" xmlns="w:g", to={{group_jid}}">
    </iq>
    '''
    def __init__(self, jid, _id = None, _type = None):
        super(GroupIqProtocolEntity, self).__init__("w:g", _id, _type, jid)