from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class PictureIqProtocolEntity(IqProtocolEntity):
    '''
    When receiving a profile picture:
    <iq type="result" from="{{jid}}" id="{{id}}">
        <picture type="image" id="{{another_id}}">
        {{Binary bytes of the picture.}}
        </picture>
    </iq>
    '''
    XMLNS = "w:profile:picture"

    def __init__(self, jid, _id = None, type = "get"):
        super(PictureIqProtocolEntity, self).__init__(self.__class__.XMLNS, _id = _id, _type=type, to = jid)