from .yowstack import YowStack

from Yowsup.layers.auth                        import YowCryptLayer, YowAuthenticatorLayer, AuthError
from Yowsup.layers.coder                       import YowCoderLayer
from Yowsup.layers.logger                      import YowLoggerLayer
from Yowsup.layers.network                     import YowNetworkLayer, NetworkError
from Yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from Yowsup.layers.packetregulator             import YowPacketRegulator
from Yowsup.layers.protocol_media              import YowMediaProtocolLayer
from Yowsup.layers.protocol_acks               import YowAckProtocolLayer
from Yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from Yowsup.layers.protocol_groups             import YowGroupsProtocolLayer


YOWSUP_FULL_STACK_DEBUG =  (
    (YowAuthenticatorLayer,
        YowMessagesProtocolLayer,
        YowMediaProtocolLayer,
        YowReceiptProtocolLayer,
        YowAckProtocolLayer,
        YowGroupsProtocolLayer),
    YowLoggerLayer,
    YowCoderLayer,
    YowCryptLayer,
    YowPacketRegulator,
    YowNetworkLayer
)

YOWSUP_FULL_STACK =  (
    (YowAuthenticatorLayer,
        YowMessagesProtocolLayer,
        YowMediaProtocolLayer,
        YowReceiptProtocolLayer,
        YowAckProtocolLayer,
        YowGroupsProtocolLayer),
    YowCoderLayer,
    YowCryptLayer,
    YowPacketRegulator,
    YowNetworkLayer
)

YOWSUP_TEXT_STACK_DEBUG =  (
    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
    YowLoggerLayer,
    YowCoderLayer,
    #YowLoggerLayer,
    YowCryptLayer,
    #YowLoggerLayer,
    YowPacketRegulator,
    YowNetworkLayer
)

YOWSUP_TEXT_STACK =  (
    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowReceiptProtocolLayer, YowAckProtocolLayer),
    YowCoderLayer,
    #YowLoggerLayer,
    YowCryptLayer,
    #YowLoggerLayer,
    YowPacketRegulator,
    YowNetworkLayer
)