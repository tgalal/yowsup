#!/usr/bin/env python
#!-*- encoding:utf-8 -*-
# debianitram .
from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.common import YowConstants
from .iq import IqProtocolEntity


class MediaIqProtocolEntity(IqProtocolEntity):

    '''
    <iq to='s.whatsapp.net' type='set' xmlns='w:m'>
        <media hash='{{b64hash}}' 
               type='{{mimetype}}' 
               size='{{size_byte}}'
               orighash='{{b64_origHash}}'>
        </media>
    </iq>
    '''

    def __init__(self, _from=None, _to=None, _id=None, _type=None, **kargs):
        super(MediaIqProtocolEntity, self).__init__(xmlns='w:m',
                                                    to=YowConstants.DOMAIN,
                                                    _type='set')
        self.setMediaProps(**kargs)

    def setMediaProps(self, **kargs):
        self.media_attribs = {'hash': kargs.get('hash'),
                              'type': kargs.get('type', 'image'),
                              'size': str(kargs.get('size'))}

        if kargs.get('orighash'):
            self.media_attribs['orighash'] = kargs.get('orighash')

    def setUrlResponse(self, **kargs):
        self.media_upload = {'url': kargs.get('url'),
                             'ip': kargs.get('ip')}

    def getUrlResponse(self):
        return self.media_upload

    def toProtocolTreeNode(self):
        node = super(MediaIqProtocolEntity, self).toProtocolTreeNode()
        mediaNode = ProtocolTreeNode('media', self.media_attribs)
        node.addChild(mediaNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = MediaIqProtocolEntity
        mediaNode = node.getChild('media')
        entity.setUrlResponse(url=mediaNode.getAttributeValue('url'),
                              ip=mediaNode.getAttributeValue('ip'))
        return entity
