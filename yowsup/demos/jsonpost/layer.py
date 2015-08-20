from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.network   import YowNetworkLayer

import datetime, sys, json, time, requests, os

class EchoLayer(YowInterfaceLayer):

    def onEvent(self, layerEvent):
        print layerEvent.getName()
        if layerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            print("Disconnected: %s" % layerEvent.getArg("reason"))
        elif layerEvent.getName() == YowNetworkLayer.EVENT_STATE_CONNECTED:
            print("Connected")

    @ProtocolEntityCallback("message")
    def onMessage(self, messageProtocolEntity):

        if messageProtocolEntity.getType() == 'text':
            self.onTextMessage(messageProtocolEntity)
        elif messageProtocolEntity.getType() == 'media':
            self.onMediaMessage(messageProtocolEntity)

        #self.toLower(messageProtocolEntity.forward(messageProtocolEntity.getFrom()))
        self.toLower(messageProtocolEntity.ack())
        self.toLower(messageProtocolEntity.ack(True))

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self, messageProtocolEntity):
        # print(dir(messageProtocolEntity))
        # 'getBody', 'getFrom', 'getId', 'getNotify', 'getParticipant', 'getTag', 'getTimestamp', 'getTo', 'getType'
        print("Received %s from %s" % (messageProtocolEntity.getBody(), messageProtocolEntity.getFrom(False)))
        self.postit(messageProtocolEntity)

    def onMediaMessage(self, messageProtocolEntity):
        # print(dir(messageProtocolEntity))
        # 'getCaption', 'getFrom', 'getId', 'getMediaSize', 'getMediaType', 'getMediaUrl', 'getMimeType', 'getNotify', 'getParticipant', 'getPreview', 'getTag', 'getTimestamp', 'getTo', 'getType',
        if messageProtocolEntity.getMediaType() == 'image':
            print("Received image %s from %s" % (messageProtocolEntity.url, messageProtocolEntity.getFrom(False)))
            self.postit(messageProtocolEntity)

    def postit(self, messageProtocolEntity):
        paramdict = {}

        if messageProtocolEntity.getType() == 'text':
            paramdict['messagecontent'] = messageProtocolEntity.getBody()
        if messageProtocolEntity.getType() == 'media' and messageProtocolEntity.getMediaType() == 'image':
            paramdict['messagecontent'] = messageProtocolEntity.getCaption()
            paramdict['url']            = messageProtocolEntity.getMediaUrl()
            paramdict['size']           = messageProtocolEntity.getMediaSize()
            paramdict['mediatype']      = messageProtocolEntity.getMediaType()
            paramdict['mimetype']       = messageProtocolEntity.getMimeType()

        paramdict['messageid']      = messageProtocolEntity.getId()
        paramdict['type']           = messageProtocolEntity.getType()
        paramdict['to']             = messageProtocolEntity.getTo()
        paramdict['from']           = messageProtocolEntity.getFrom(False)
        paramdict['notify']         = messageProtocolEntity.getNotify()
        paramdict['participant']    = messageProtocolEntity.getParticipant()
        paramdict['timestamp']      = messageProtocolEntity.getTimestamp()
        paramdict['tag']            = messageProtocolEntity.getTag()
                
        post_data = json.dumps(paramdict)
        print post_data
        # get http post endpoint url from environment var
        url = os.environ['URL']
        r = requests.post(url, post_data)
        print r.status_code
        print r.headers
