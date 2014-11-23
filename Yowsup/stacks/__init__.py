from .yowstack import YowStack

from Yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from Yowsup.layers.coder                       import YowCoderLayer
from Yowsup.layers.logger                      import YowLoggerLayer
from Yowsup.layers.network                     import YowNetworkLayer, NetworkError
from Yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from Yowsup.layers.stanzaregulator             import YowStanzaRegulator
from Yowsup.layers.protocol_media              import YowMediaProtocolLayer
from Yowsup.layers.protocol_acks               import YowAckProtocolLayer
from Yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from Yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from Yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from Yowsup.layers.protocol_ib                 import YowIbProtocolLayer
from Yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from Yowsup.layers.protocol_iq                 import YowIqProtocolLayer



YOWSUP_CORE_LAYERS = (
    YowCoderLayer,
    YowCryptLayer,
    YowStanzaRegulator,
    YowNetworkLayer
)


YOWSUP_PROTOCOL_LAYERS_BASIC = (
    YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
    YowReceiptProtocolLayer, YowAckProtocolLayer, YowPresenceProtocolLayer,
    YowIbProtocolLayer, YowIqProtocolLayer, YowNotificationsProtocolLayer
)

YOWSUP_PROTOCOL_LAYERS_GROUPS = (YowGroupsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_MEDIA  = (YowMediaProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_FULL = (YowGroupsProtocolLayer, YowMediaProtocolLayer) + YOWSUP_PROTOCOL_LAYERS_BASIC


YOWSUP_FULL_STACK_DEBUG = (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                           (YowLoggerLayer,) +\
                           YOWSUP_CORE_LAYERS

YOWSUIP_FULL_STACK = (YOWSUP_PROTOCOL_LAYERS_FULL) +\
                     YOWSUP_CORE_LAYERS
