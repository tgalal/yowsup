from .yowstack import YowStack

from Yowsup.layers.auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from Yowsup.layers.coder              import YowCoderLayer
from Yowsup.layers.logger             import YowLoggerLayer
from Yowsup.layers.network            import YowNetworkLayer, NetworkError
from Yowsup.layers.messages           import YowMessagesProtocolLayer
from Yowsup.layers.packetregulator    import YowPacketRegulator
from Yowsup.layers.media              import YowMediaProtocolLayer
from Yowsup.layers.acks               import YowAckProtocolLayer
from Yowsup.layers.receipts           import YowReceiptProtocolLayer

YOWSUP_FULL_STACK =  (
    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowMediaProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
    YowLoggerLayer,
    YowCoderLayer,
    YowCryptLayer,
    YowPacketRegulator,
    YowNetworkLayer
)

YOWSUP_TEXT_STACK =  (
    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
    YowLoggerLayer,
    YowCoderLayer,
    #YowLoggerLayer,
    YowCryptLayer,
    #YowLoggerLayer,
    YowPacketRegulator,
    YowNetworkLayer
)