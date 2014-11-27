from yowsup.layers import YowLayer, YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
class YowStanzaRegulator(YowLayer):
    '''
        send:       bytearray -> bytearray
        receive:    bytearray -> bytearray
    '''

    def __init__(self):
        super(YowLayer, self).__init__()
        self.buf = bytearray()
        self.enabled = False

    def onEvent(self, yowLayerEvent):
        if yowLayerEvent.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            self.enabled = True
            self.buf = bytearray()
        elif yowLayerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            self.enabled = False


    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        if self.enabled:
            self.buf.extend(data)
            self.processReceived()
        else:
            self.toLower(data)


    def processReceived(self):
        metaData = self.buf[:3]
        recvData = self.buf[3:]

        firstByte = metaData[0]
        stanzaFlag = (firstByte & 0xF0) >> 4
        stanzaSize =  ((metaData[1] << 8) + metaData[2])  | ((firstByte & 0x0F) << 16)

        if len(recvData) < stanzaSize:
            #will in leave in buf till receive remaining data
            return

        oneMessageData = metaData + recvData[:stanzaSize]
        self.buf = self.buf[len(oneMessageData):]

        self.toUpper(oneMessageData)

        if len(self.buf) > 3: #min required if has processable data yet
            self.processReceived()

    def __str__(self):
        return "Stanza Regulator Layer"







