# Based heavily on https://github.com/axel-angel/whatsapp-email-bridge, but using twisted
from yowsup.layers.interface import YowInterfaceLayer
from yowsup.layers.interface import ProtocolEntityCallback
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from twisted.internet import protocol, endpoints, defer
from twisted.internet import reactor
from twisted.mail.smtp import ESMTPSenderFactory
from twisted.mail.smtp import SMTPSenderFactory


import datetime, sys

from email.mime.text import MIMEText
from email.utils import formatdate
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO


import logging
logger = logging.getLogger(__name__)


class YowTwistedSmtpLayer(YowInterfaceLayer):
    PROP_ENDPOINT           = "org.openwhatsapp.yowsup.prop.smtp.endpoint"
    PROP_USER               = "org.openwhatsapp.yowsup.prop.smtp.user"
    PROP_PASS               = "org.openwhatsapp.yowsup.prop.smtp.pass"
    PROP_DST_MAIL           = "org.openwhatsapp.yowsup.prop.dst_mail"
    PROP_REPLY_MAIL         = "org.openwhatsapp.yowsup.prop.reply_mail"

    def __str__(self):
        return "Twisted Smtp Layer"

    @ProtocolEntityCallback("message")
    def onMessage(self, mEntity):
        print( "----------> ", mEntity )
        if not mEntity.isGroupMessage():
            if mEntity.getType() == 'text':
                self.onTextMessage(mEntity)
            elif mEntity.getType() == 'media':
                self.onMediaMessage(mEntity)
        else:
            src = mEntity.getFrom()
            print("<= WhatsApp: <- %s GroupMessage" % (src))
        self.toLower(mEntity.ack())
        self.toLower(mEntity.ack(True))


    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    def onTextMessage(self, mEntity):
        print("Echoing %s to %s" % (mEntity.getBody(), mEntity.getFrom(False)))
        receipt = OutgoingReceiptProtocolEntity(mEntity.getId(), mEntity.getFrom())
        src = mEntity.getFrom()
        print("<= WhatsApp: <- %s Message" % (src))

        content = mEntity.getBody()
        self.sendEmail(mEntity, content, content)
        self.toLower(receipt)

    def onMediaMessage(self, mEntity):
        if mEntity.getMediaType() == "image":
            print("Echoing image %s to %s" % (mEntity.url, mEntity.getFrom(False)))
        elif mEntity.getMediaType() == "location":
            print("Echoing location (%s, %s) to %s" % (mEntity.getLatitude(), mEntity.getLongitude(), mEntity.getFrom(False)))
        elif mEntity.getMediaType() == "vcard":
            print("Echoing vcard (%s, %s) to %s" % (mEntity.getName(), mEntity.getCardData(), mEntity.getFrom(False)))

        id = mEntity.getId()
        src = mEntity.getFrom()
        tpe = mEntity.getMediaType()
        url = getattr(mEntity, 'url', None)

        print("<= WhatsApp: <- Media %s (%s)" % (tpe, src))

        content = "Received a media of type: %s\n" % (tpe)
        content += "URL: %s\n" % (url)
        content += str(mEntity)
        self.sendEmail(mEntity, "Media: %s" % (tpe), content)

        receipt = OutgoingReceiptProtocolEntity(id, src)
        self.toLower(receipt)


    def sendEmail(self, mEntity, subject, content):
        #self.dst_phone = self.getProp(self.__class__.PROP_DST_PHONE)

        timestamp = mEntity.getTimestamp()
        srcShort = mEntity.getFrom(full = False)

        formattedDate = datetime.datetime.fromtimestamp(timestamp) \
                                         .strftime('%d/%m/%Y %H:%M')
        content2 = "%s\n\nAt %s by %s (%s) isBroadCast=%s" \
                % (content, formattedDate, srcShort, mEntity.getParticipant(),
                    mEntity.isBroadcast())

        smtp_user = self.getProp(self.__class__.PROP_USER )
        dst_mail = self.getProp(self.__class__.PROP_DST_MAIL)
        reply_mail = self.getProp(self.__class__.PROP_REPLY_MAIL, None)
        msg = MIMEText(content2, 'plain', 'utf-8')
        msg['To'] = "WhatsApp <%s>" % (dst_mail)
        msg['From'] = "%s <%s>" % (srcShort, mEntity.getParticipant())
        msg['Reply-To'] = "%s <%s>" % (mEntity.getParticipant(), reply_mail)
        msg['Subject'] = subject
        msg['Date'] = formatdate(timestamp)
        msg_file = StringIO(msg.as_string())

        def success(r):
            print("Mail sent")
        def error(err):
            err.printTraceback()
            print("Smtp error ", err)

        dfr = defer.Deferred()
        dfr.addCallback(success)
        dfr.addErrback(error)
        if smtp_user:
            smtp_pass = self.getProp(self.__class__.PROP_PASS )
            factory = ESMTPSenderFactory(smtp_user, smtp_pass, reply_mail, dst_mail, msg_file, dfr)
        else:
            factory = SMTPSenderFactory(reply_mail, dst_mail, msg_file, dfr)

        endpoint = self.getProp(self.__class__.PROP_ENDPOINT)
        smtp_endpoint = endpoints.clientFromString(reactor, endpoint)
        smtp_endpoint.connect(factory)


        #s.sendmail(dst, [dst], msg.as_string())
        print("=> Mail: %s -> %s" % (reply_mail, dst_mail))

