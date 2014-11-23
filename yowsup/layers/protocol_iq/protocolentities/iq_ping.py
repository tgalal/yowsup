from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq import IqProtocolEntity
class PingIqProtocolEntity(IqProtocolEntity):

    '''
    Receive
    <iq type="get" xmlns="urn:xmpp:ping" from="s.whatsapp.net" id="1416174955-ping">
    </iq>
    Send
    <iq type="get" xmlns="w:p" to="s.whatsapp.net" id="1416174955-ping">
    </iq>
    '''

    def __init__(self, _from = None, to = None, _id = None):
        super(PingIqProtocolEntity, self).__init__("urn:xmpp:ping" if _from else "w:p", _id = _id, _type = "get", _from = _from, to = to)
