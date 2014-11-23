from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_result import ResultIqProtocolEntity
class PongResultIqProtocolEntity(ResultIqProtocolEntity):

    '''
    <iq type="result" xmlns="w:p" to="self.domain" id="1416174955-ping">
    </iq>
    '''
    def __init__(self, to, _id = None):
        super(PongResultIqProtocolEntity, self).__init__("w:p", _id = _id, to = to)
