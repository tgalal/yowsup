from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .presence import PresenceProtocolEntity
class UnavailablePresenceProtocolEntity(PresenceProtocolEntity):
    '''
    <presence type="unavailable"></presence>
    response:
    <presence type="unavailable" from="self.jid">
    </presence>
    '''
    def __init__(self):
        super(UnavailablePresenceProtocolEntity, self).__init__("unavailable")