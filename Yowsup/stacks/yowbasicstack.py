from Yowsup.layers.auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from Yowsup.layers.coder              import YowCoderLayer
from Yowsup.layers.logger             import YowLoggerLayer
from Yowsup.layers.network            import YowNetworkLayer, NetworkError
from Yowsup.layers.protocol           import YowProtocolLayer
from Yowsup.layers.packetregulator    import YowPacketRegulator
from Yowsup.layers.media              import YowMediaPictureLayer

from yowstack import YowStack

class YowBasicStack(YowStack):
    def __init__(self):
        YowStack.__init__(self,
            [ 
                YowNetworkLayer,
                YowPacketRegulator,
                YowCryptLayer,
                YowCoderLayer,
                YowAuthenticatorLayer,
                YowMediaPictureLayer,
                YowProtocolLayer,
                
            ]
        )
