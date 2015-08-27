from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.protocol_messages.protocolentities import TextMessageProtocolEntity
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.interface                          import ProtocolEntityCallback
from yowsup.layers.network.layer import YowNetworkLayer
from twisted.internet import protocol, endpoints, task, defer
from twisted.internet import reactor
from twisted.mail import imap4
from email.parser import Parser

import threading
import base64
import logging
logger = logging.getLogger(__name__)


class YowTwistedImapLayer(YowInterfaceLayer):
    PROP_ENDPOINT           = "org.openwhatsapp.yowsup.prop.imap.endpoint"
    PROP_USER               = "org.openwhatsapp.yowsup.prop.imap.user"
    PROP_PASS               = "org.openwhatsapp.yowsup.prop.imap.pass"
    PROP_POOLINTERVAL       = "org.openwhatsapp.yowsup.prop.imap.pool_interval"
    PROP_DST_PHONE          = "org.openwhatsapp.yowsup.prop.dst_phone"

    #EVENT_INMSG             = "org.openwhatsapp.yowsup.event.imap.message"

    def __init__(self):
        super(YowTwistedImapLayer, self).__init__()
        self.ackQueue = []
        self.lock = threading.Condition()

    ### standard layer methods ###
    def onEvent(self, yowLayerEvent):
        if yowLayerEvent.getName() == YowNetworkLayer.EVENT_STATE_CONNECT:
            self.imap_factory = protocol.Factory()
            self.imap_factory.protocol = imap4.IMAP4Client
            endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
            self.imap_endpoint = endpoints.clientFromString(reactor, endpoint)
            pool_interval = self.getProp(self.__class__.PROP_POOLINTERVAL, 60 * 10)
            task.LoopingCall(self.imap_pooling).start(pool_interval, now=True).addErrback(self.periodic_task_crashed)
        elif yowLayerEvent.getName() == YowNetworkLayer.EVENT_STATE_DISCONNECTED:
            pass
        return super( YowInterfaceLayer, self ).onEvent(yowLayerEvent)

    def __str__(self):
        return "Twisted Imap Layer"

    def periodic_task_crashed(self, err):
        logger.error("periodic_task broken %s", err)

    @defer.inlineCallbacks
    def imap_pooling(self):
        # Todo: errors in defer
        logger.debug("fetching mails")
        client = yield self.imap_endpoint.connect(self.imap_factory)
        imap_user = self.getProp(self.__class__.PROP_USER)
        imap_pass = self.getProp(self.__class__.PROP_PASS)
        yield client.login(imap_user, imap_pass)
        inbox = yield client.select('INBOX')

        ids = yield client.search( imap4.Query( unseen=True ), uid=True )

        phone = self.getProp(self.__class__.PROP_DST_PHONE)
        if '@' in phone:
            to = phone
        elif '-' in phone:
            to = "%s@g.us" % phone
        else:
            to = "%s@s.whatsapp.net" % phone

        for id in ids:
            msgs = yield client.fetchMessage( id, uid=True )
            for k in msgs:
                #print "----------> POOL ", msgs[k]['RFC822']
                self.send_yowsup(to, msgs[k]['RFC822'])
                # todo: must mask as readed on yowsup ack, need a queue for that!!!
                yield client.addFlags( id, "Seen",  uid=True)
        yield client.logout()

    def send_yowsup(self, phone, data):
        m = Parser().parsestr(data)
        try:
            txt = self.mail_to_txt(m)
        except Exception as e:
            logger.error( "501 malformed content: %s" % (str(e)) )

        # send text, if any
        if len(txt.strip()) > 0:
            msg = TextMessageProtocolEntity(txt, to = phone)
            print("=> WhatsApp: %s -> %s" % (phone,msg))
            self.toLower(msg)

        # send media that were attached pieces
        if m.is_multipart():
            for pl in getattr(m, '_payload', []):
                self.handle_forward_media(phone, pl)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        ack = OutgoingAckProtocolEntity(entity.getId(), "receipt",
                entity.getType(), entity.getFrom())
        self.toLower(ack)

    def mail_to_txt(self,m):
        if not m.is_multipart():
            # simple case for text/plain
            return self.mail_payload_decoded(m)

        else:
            # handle when there are attachements (take first text/plain)
            for pl in m._payload:
                if "text/plain" in pl.get('Content-Type', None):
                    return self.mail_payload_decoded(pl)
            # otherwise take first text/html
            for pl in m._payload:
                if "text/html" in pl.get('Content-Type', None):
                    return html2text(self.mail_payload_decoded(pl))
            # otherwise search into recursive message
            for pl in m._payload:
                try:
                    if "multipart/alternative" in pl.get('Content-Type', None):
                        return self.mail_to_txt(pl)
                except:
                    continue # continue to next attachment
            raise Exception("No text could be extracted found")

    def mail_payload_decoded(self,pl):
        t = pl.get_payload()
        if pl.get('Content-Transfer-Encoding', None) == "base64":
            t = base64.b64decode(t)
        return t

    def handle_forward_media(self, jid, pl):
        ct = pl.get('Content-Type', 'None')
        ct1 = ct.split('/', 1)[0]
        iqtp = None
        if ct1 == 'text':
            return # this is the body, probably
        if ct1 == 'image':
            iqtp = RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE
        if ct1 == 'audio':
            iqtp = RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO
        if ct1 == 'video':
            iqtp = RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO
        if ct.startswith('multipart/alternative'): # recursive content
            for pl2 in pl._payload:
                self.handle_forward_media(jid, pl2)
        if iqtp == None:
            print("<= Mail: Skip unsupported attachement type %s" % (ct))
            return

        print("<= Mail: Forward attachement %s" % (ct1))
        data = self.mail_payload_decoded(pl)
        tmpf = tempfile.NamedTemporaryFile(prefix='whatsapp-upload_',
                delete=False)
        tmpf.write(data)
        tmpf.close()
        fpath = tmpf.name
        # FIXME: need to close the file!

        entity = RequestUploadIqProtocolEntity(iqtp, filePath=fpath)
        def successFn(successEntity, originalEntity):
            return self.onRequestUploadResult(
                    jid, fpath, successEntity, originalEntity)
        def errorFn(errorEntity, originalEntity):
            return self.onRequestUploadError(
                    jid, fpath, errorEntity, originalEntity)

        self._sendIq(entity, successFn, errorFn)

    def onRequestUploadResult(self, jid, fpath, successEntity, originalEntity):
        if successEntity.isDuplicate():
            url = successEntity.getUrl()
            ip = successEntity.getIp()
            print("<= WhatsApp: upload duplicate %s, from %s" % (fpath, url))
            self.send_uploaded_media(fpath, jid, url, ip)
        else:
            ownjid = self.getOwnJid()
            mediaUploader = MediaUploader(jid, ownjid, fpath,
                                      successEntity.getUrl(),
                                      successEntity.getResumeOffset(),
                                      self.onUploadSuccess,
                                      self.onUploadError,
                                      self.onUploadProgress,
                                      async=False)
            print("<= WhatsApp: start upload %s, into %s" \
                    % (fpath, successEntity.getUrl()))
            mediaUploader.start()

    def onUploadSuccess(self, fpath, jid, url):
        print("WhatsApp: -> upload success %s" % (fpath))
        self.send_uploaded_media(fpath, jid, url)

    def onUploadError(self, fpath, jid=None, url=None):
        print("WhatsApp: -> upload failed %s" % (fpath))
        ownjid = self.getOwnJid()
        fakeEntity = TextMessageProtocolEntity("", _from = ownjid)
        self.sendEmail(fakeEntity, "WhatsApp upload failed",
                "File: %s" % (fpath))

    def onUploadProgress(self, fpath, jid, url, progress):
        print("WhatsApp: -> upload progression %s for %s, %d%%" \
                % (fpath, jid, progress))

    def send_uploaded_media(self, fpath, jid, url, ip = None):
        entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(
                fpath, url, ip, jid)
        self.toLower(entity)

    def onRequestUploadError(self, jid, fpath, errorEntity, originalEntity):
        print("WhatsApp: -> upload request failed %s" % (fpath))
        self.sendEmail(errorEntity, "WhatsApp upload request failed",
                "File: %s" % (fpath))


