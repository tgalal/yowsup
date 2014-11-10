from Yowsup.layers.auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from Yowsup.layers.coder              import YowCoderLayer
from Yowsup.layers.logger             import YowLoggerLayer
from Yowsup.layers.network            import YowNetworkLayer, NetworkError
from Yowsup.layers.messages           import YowMessagesProtocolLayer
from Yowsup.layers.packetregulator    import YowPacketRegulator
from Yowsup.layers.media              import YowMediaProtocolLayer
# from Yowsup.layers.interface          import YowInterfaceLayer
from Yowsup.layers.interface_cli      import YowCliInterfaceLayer


from .yowstack import YowStack

class YowBasicStack(YowStack):
    def __init__(self):
        super(YowBasicStack, self).__init__(
                (
                    YowCliInterfaceLayer,
                    #YowLoggerLayer,
                    (YowAuthenticatorLayer, YowMessagesProtocolLayer, YowMediaProtocolLayer),
                    YowLoggerLayer,
                    YowCoderLayer,
                    #YowLoggerLayer,
                    YowCryptLayer,
                    #YowLoggerLayer,
                    YowPacketRegulator,
                    # YowLoggerLayer,
                    YowNetworkLayer
                )
            )
