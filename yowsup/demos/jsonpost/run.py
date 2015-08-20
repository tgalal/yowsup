from yowsup.stacks import YowStack
from layer import EchoLayer
from yowsup.layers import YowLayerEvent
from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.axolotl                     import YowAxolotlLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.common import YowConstants
from yowsup import env

import logging
#logging.basicConfig(level=logging.DEBUG)

import os
# get credentials from environment vars
CREDENTIALS = (os.environ['PHONE'], os.environ['PASSWORD'])

if __name__ == "__main__":
    encryptionEnabled = False
    if encryptionEnabled:
        layers = (
            EchoLayer,
            (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer),
            YowAxolotlLayer,
            YowLoggerLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )
    else:
        env.CURRENT_ENV = env.S40YowsupEnv()
        layers = (
            EchoLayer,
            (YowAuthenticationProtocolLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer, YowMediaProtocolLayer, YowIqProtocolLayer, YowCallsProtocolLayer),
            YowLoggerLayer,
            YowCoderLayer,
            YowCryptLayer,
            YowStanzaRegulator,
            YowNetworkLayer
        )

    stack = YowStack(layers)
    stack.setProp(YowAuthenticationProtocolLayer.PROP_CREDENTIALS, CREDENTIALS)
    stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0])
    stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
    stack.setProp(YowCoderLayer.PROP_RESOURCE, env.CURRENT_ENV.getResource())

    stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
    try:
        stack.loop(timeout = 0.5, discrete = 0.5)
    except AuthError as e:
        print("Authentication Error: %s" % e.message)
