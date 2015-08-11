from twisted.internet import reactor
from yowsup.stacks import YowStack
from yowsup.layers import YowLayerEvent
from yowsup.layers import YowParallelLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.network_twisted             import YowTwistedNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.layers.imap_twisted                import YowTwistedImapLayer
from yowsup.layers.smtp_twisted                import YowTwistedSmtpLayer
from yowsup.common import YowConstants
from yowsup import env

class YowsupImapBridgeStack(object):

    def __init__(self, imap_data, smtp_data, credentials, encryptionEnabled = False):
        if encryptionEnabled:
            layers = (
                YowParallelLayer( (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer ), ), 
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowTwistedNetworkLayer
            )
        else:
            env.CURRENT_ENV = env.S40YowsupEnv()
            layers = (
                YowParallelLayer( (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer), ),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowTwistedNetworkLayer
            )

        if smtp_data:
            layers = (YowTwistedSmtpLayer,) + layers

        if imap_data:
            layers = (YowTwistedImapLayer,) + layers

        self.stack = YowStack(layers)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, credentials)
        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())

        if smtp_data:
            self.stack.setProp(YowTwistedSmtpLayer.PROP_USER, smtp_data[0])
            self.stack.setProp(YowTwistedSmtpLayer.PROP_PASS, smtp_data[1])
            self.stack.setProp(YowTwistedSmtpLayer.PROP_ENDPOINT, smtp_data[2])
            self.stack.setProp(YowTwistedSmtpLayer.PROP_DST_MAIL, smtp_data[3])
            self.stack.setProp(YowTwistedSmtpLayer.PROP_REPLY_MAIL, smtp_data[4])

        if imap_data:
            self.stack.setProp(YowTwistedImapLayer.PROP_USER, imap_data[0])
            self.stack.setProp(YowTwistedImapLayer.PROP_PASS, imap_data[1])
            self.stack.setProp(YowTwistedImapLayer.PROP_ENDPOINT, imap_data[2])
            self.stack.setProp(YowTwistedImapLayer.PROP_DST_PHONE, imap_data[3])

    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            reactor.run()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)




