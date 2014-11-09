from Yowsup.layers.auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from Yowsup.layers.coder              import YowCoderLayer
from Yowsup.layers.logger             import YowLoggerLayer
from Yowsup.layers.network            import YowNetworkLayer, NetworkError
#from Yowsup.layers.protocol           import YowProtocolLayer
from Yowsup.layers.messages           import YowMessagesProtocolLayer
from Yowsup.layers.groupmessages      import YowGroupMessagesProtocolLayer
from Yowsup.layers.packetregulator    import YowPacketRegulator
from Yowsup.layers.media              import YowMediaPictureLayer
from Yowsup.layers.interface          import YowInterfaceLayer


from .yowstack import YowStack

class YowBasicStack(YowStack):
    def __init__(self):
        super(YowBasicStack, self).__init__(
                (
                    YowInterfaceLayer,
                    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowGroupMessagesProtocolLayer),
                    YowLoggerLayer,
                    YowCoderLayer,
                    YowLoggerLayer,
                    YowCryptLayer,
                    YowLoggerLayer,
                    YowPacketRegulator,
                    YowNetworkLayer
                )
            )
