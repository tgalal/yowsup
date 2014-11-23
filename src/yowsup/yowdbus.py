from auth               import YowCryptLayer, YowAuthenticatorLayer, AuthError
from coder              import YowCoderLayer
from logger             import YowLoggerLayer
from network            import YowNetworkLayer, NetworkError
from protocol           import YowProtocolLayer
from packetregulator    import YowPacketRegulator
import asyncore, sys, traceback, base64


ENDPOINT_REMOTE = ("c2.whatsapp.net", 443)

class YowStackInit:
    def __init__(self):
        stack = (
            YowNetworkLayer,
            YowPacketRegulator,
            #YowLoggerLayer,
            YowCryptLayer,
            #YowLoggerLayer,
            YowCoderLayer,
            YowLoggerLayer,
            YowProtocolLayer,
            YowAuthenticatorLayer
            )

        stack_instances = []

        print("Initialzing stack")
        for s in stack:
            print("Constructing %s" %s)
            stack_instances.append(s())

        YowNetworkLayer.setProp("endpoint", ENDPOINT_REMOTE)
        YowCoderLayer.setProp("domain", "s.whatsapp.net")
        YowCoderLayer.setProp("resource", "S40-2.12.15")


        for i in range(0, len(stack_instances)):
            upperLayer = stack_instances[i + 1] if (i + 1) < len(stack_instances) else None
            lowerLayer = stack_instances[i - 1] if i > 0 else None
            stack_instances[i].setLayers(upperLayer, lowerLayer)

        try:
            asyncore.loop()
        except NetworkError, e:
            print("NetworkError, reason: %s, exiting" % e)
            sys.exit(1)
        except AuthError, e:
            print("Auth Error, reason %s" % e)
            sys.exit(1)
        except KeyboardInterrupt, e:
            print("\nYowsdown")
            sys.exit(0)

