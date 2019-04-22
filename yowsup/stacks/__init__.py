from .yowstack import YowStack, YowStackBuilder

from yowsup.layers.auth                        import YowAuthenticationProtocolLayer
from yowsup.layers.coder                       import YowCoderLayer
from yowsup.layers.logger                      import YowLoggerLayer
from yowsup.layers.network                     import YowNetworkLayer
from yowsup.layers.protocol_messages           import YowMessagesProtocolLayer
from yowsup.layers.protocol_media              import YowMediaProtocolLayer
from yowsup.layers.protocol_acks               import YowAckProtocolLayer
from yowsup.layers.protocol_receipts           import YowReceiptProtocolLayer
from yowsup.layers.protocol_groups             import YowGroupsProtocolLayer
from yowsup.layers.protocol_presence           import YowPresenceProtocolLayer
from yowsup.layers.protocol_ib                 import YowIbProtocolLayer
from yowsup.layers.protocol_notifications      import YowNotificationsProtocolLayer
from yowsup.layers.protocol_iq                 import YowIqProtocolLayer
from yowsup.layers.protocol_contacts           import YowContactsIqProtocolLayer
from yowsup.layers.protocol_chatstate          import YowChatstateProtocolLayer
from yowsup.layers.protocol_privacy            import YowPrivacyProtocolLayer
from yowsup.layers.protocol_profiles           import YowProfilesProtocolLayer
from yowsup.layers.protocol_calls              import YowCallsProtocolLayer
from yowsup.layers.noise.layer                 import YowNoiseLayer
from yowsup.layers.noise.layer_noise_segments  import YowNoiseSegmentsLayer



YOWSUP_CORE_LAYERS = (
    YowLoggerLayer,
    YowCoderLayer,
    YowNoiseLayer,
    YowNoiseSegmentsLayer,
    YowNetworkLayer
)


YOWSUP_PROTOCOL_LAYERS_BASIC = (
    YowAuthenticationProtocolLayer, YowMessagesProtocolLayer,
    YowReceiptProtocolLayer, YowAckProtocolLayer, YowPresenceProtocolLayer,
    YowIbProtocolLayer, YowIqProtocolLayer, YowNotificationsProtocolLayer,
    YowContactsIqProtocolLayer, YowChatstateProtocolLayer

)

YOWSUP_PROTOCOL_LAYERS_GROUPS = (YowGroupsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_MEDIA  = (YowMediaProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_PROFILES  = (YowProfilesProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_CALLS  = (YowCallsProtocolLayer,) + YOWSUP_PROTOCOL_LAYERS_BASIC
YOWSUP_PROTOCOL_LAYERS_FULL = (YowGroupsProtocolLayer, YowMediaProtocolLayer, YowPrivacyProtocolLayer, YowProfilesProtocolLayer, YowCallsProtocolLayer)\
                              + YOWSUP_PROTOCOL_LAYERS_BASIC


YOWSUP_FULL_STACK = (YOWSUP_PROTOCOL_LAYERS_FULL,) +\
                     YOWSUP_CORE_LAYERS
