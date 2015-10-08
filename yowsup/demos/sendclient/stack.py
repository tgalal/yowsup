from yowsup.stacks import YowStack
from .layer import SendLayer
from yowsup.layers import YowLayerEvent, YowParallelLayer
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.common import YowConstants
from yowsup import env
import sys

class YowsupSendStack(object):
    def __init__(self, credentials, messages, encryptionEnabled = False):
        """
        :param credentials:
        :param messages: list of (jid, message) tuples
        :param encryptionEnabled:
        :return:
        """
        sendLayer = SendLayer()
        if encryptionEnabled:
            from yowsup.layers.axolotl                     import YowAxolotlLayer
            layers = (
                sendLayer,
                YowParallelLayer([
                    YowAuthenticationProtocolLayer,
                    YowMessagesProtocolLayer,
                    YowReceiptProtocolLayer,
                    YowAckProtocolLayer]),
                YowAxolotlLayer,
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )
        else:
            layers = (
                sendLayer,
                YowParallelLayer([
                    YowAuthenticationProtocolLayer,
                    YowMessagesProtocolLayer,
                    YowReceiptProtocolLayer,
                    YowAckProtocolLayer]),
                YowLoggerLayer,
                YowCoderLayer,
                YowCryptLayer,
                YowStanzaRegulator,
                YowNetworkLayer
            )

        self.sendLayer = sendLayer
        self.stack = YowStack(layers)
        self.stack.setProp(SendLayer.PROP_MESSAGES, messages)
        self.stack.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)
        self.stack.setCredentials(credentials)

    def start(self):
        sendLayer = self.sendLayer
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
        except KeyboardInterrupt:
            pass
        sys.exit(0 if sendLayer.acked else 1)
