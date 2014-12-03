from .yowstack import YowStack

from yowsup.layers.auth                        import YowCryptLayer, YowAuthenticationProtocolLayer, AuthError
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.stanzaregulator             import YowStanzaRegulator
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.layers.protocol_ib                 import YowIbProtocolLayer
from yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_contacts           import YowContactsIqProtocolLayer



YOWSUP_CORE_LAYERS = (
    YowCoderLayer,
    YowCryptLayer,
    YowStanzaRegulator,
    YowNetworkLayer
)


YOWSUP_PROTOCOL_LAYERS_BASIC = (
    YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
    YowReceiptProtocolLayer, YowAckProtocolLayer, YowPresenceProtocolLayer,
    YowIbProtocolLayer, YowIqProtocolLayer, YowNotificationsProtocolLayer,
    YowContactsIqProtocolLayer

)

YOWSUP_PROTOCOL_LAYERS_GROUPS = (YowGroupsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_MEDIA  = (YowMediaProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_FULL = (YowGroupsProtocolLayer, YowMediaProtocolLayer) + YOWSUP_PROTOCOL_LAYERS_BASIC


YOWSUP_FULL_STACK_DEBUG = (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                           (YowLoggerLayer,) +\
                           YOWSUP_CORE_LAYERS

YOWSUIP_FULL_STACK = (YOWSUP_PROTOCOL_LAYERS_FULL) +\
                     YOWSUP_CORE_LAYERS
