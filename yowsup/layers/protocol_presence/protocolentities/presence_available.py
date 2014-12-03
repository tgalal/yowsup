from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .presence import PresenceProtocolEntity
class AvailablePresenceProtocolEntity(PresenceProtocolEntity):
    '''
    <presence type="available"></presence>
    response:
    <presence from="self.jid">
    </presence>

    '''
    def __init__(self):
        super(AvailablePresenceProtocolEntity, self).__init__("available")