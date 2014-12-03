from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq import IqProtocolEntity
class ResultIqProtocolEntity(IqProtocolEntity):

    '''
    <iq type="result" id="{{id}}" from={{FROM}}">
    </iq>
    '''

    def __init__(self, xmlns, _id = None, to = None, _from = None):
        super(ResultIqProtocolEntity, self).__init__(xmlns, _id = _id, _type = "result", to = to, _from = _from)

