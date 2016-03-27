from yowsup.layers import YowLayer, EventCallback
from yowsup.layers.network import YowNetworkLayer
class YowCryptLayer(YowLayer):
    '''
        send:       bytearray -> bytearray
        receive:    bytearray -> bytearray
    '''

    EVENT_KEYS_READY = "org.openwhatsapp.yowsup.crypt.keys"

    def __init__(self):
        super(YowCryptLayer, self).__init__()
        self.keys = (None,None)

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, yowLayerEvent):
        self.keys = (None,None)
    
    @EventCallback(EVENT_KEYS_READY)
    def onKeysReady(self, yowLayerEvent):
        self.keys = yowLayerEvent.getArg("keys")
        return True

    def send(self, data):
        outputKey = self.keys[1]
        length1 = len(data)
        if length1 > 1:
            if outputKey:
                length1 += 4
                buf = outputKey.encodeMessage(data, len(data), 0, len(data))
                res = [0,0,0]
                res.extend(buf)
                res[0] = ((8 << 4) | (length1 & 16711680) >> 16) % 256
                res[1] = ((length1 & 65280) >> 8) % 256
                res[2] = (length1 & 255) % 256
                

                data = res

            else:
                prep = [0,0,0]
                prep.extend(data)
                prep[0] = ((0 << 4) | (length1 & 16711680) >> 16) % 256
                prep[1] = ((length1 & 65280) >> 8) % 256
                prep[2] = (length1 & 255) % 256
                data = prep

        self.toLower(bytearray(data))

    def receive(self, data):
        inputKey = self.keys[0]
        metaData = data[:3]
        payload = bytearray(data[3:])

        firstByte = metaData[0]
        stanzaFlag = (firstByte & 0xF0) >> 4
        stanzaSize =  ((metaData[1] << 8) + metaData[2])  | ((firstByte & 0x0F) << 16)
        isEncrypted = ((stanzaFlag & 8) != 0)


        if inputKey and isEncrypted:
            toDecode = data[3:]
            payload = inputKey.decodeMessage(payload, 0, 4, len(payload) - 4)

        self.toUpper(payload)

    def __str__(self):
        return "Crypt Layer"