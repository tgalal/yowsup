from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class PictureIqProtocolEntity(IqProtocolEntity):
    '''
    <iq type="{{get | set?}}" id="{{id}}" xmlns="w:profile:picture", to={{group_jid}}">
    </iq>
    '''
    def __init__(self, to = None,  _id = None, _type = None):
        super(PictureIqProtocolEntity, self).__init__("w:profile:picture", _id, _type, to = to)