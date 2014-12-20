
from ..ecc.curve import Curve
from ..ecc.eckeypair import ECKeyPair
from ..ecc.djbec import *
from ..identitykey import IdentityKey
from ..identitykeypair import IdentityKeyPair
from ..state.prekeyrecord import PreKeyRecord
from ..state.signedprekeyrecord import SignedPreKeyRecord
from medium import Medium
import os
import struct
import time
import binascii


class KeyHelper:

    def __init__(self):
        pass

    """
    Generate an identity key pair.  Clients should only do this once,
    at install time.
    @return the generated IdentityKeyPair.
    """
    @staticmethod
    def generateIdentityKeyPair():
        keyPair   = Curve.generateKeyPair()
        publicKey = IdentityKey(keyPair.getPublicKey())
        serialized = '0a21056e8936e8367f768a7bba008ade7cf58407bdc7a6aae293e2cb7c06668dcd7d5e12205011524f0c15467100dd6' \
                     '03e0d6020f4d293edfbcd82129b14a88791ac81365c'
        serialized = binascii.unhexlify(serialized)
        return IdentityKeyPair(publicKey, keyPair.getPrivateKey())
        #return IdentityKeyPair(serialized=serialized)

    """
    Generate a registration ID.  Clients should only do this once,
    at install time.
    """
    @staticmethod
    def generateRegistrationId():
        return KeyHelper.generateRandomSequence()

    @staticmethod
    def generateRandomSequence():
        return abs(struct.unpack('>i', bytearray(os.urandom(4)))[0])


    """
    Generate a list of PreKeys.  Clients should do this at install time, and
    subsequently any time the list of PreKeys stored on the server runs low.

    PreKey IDs are shorts, so they will eventually be repeated.  Clients should
    store PreKeys in a circular buffer, so that they are repeated as infrequently
    as possible.

    @param start The starting PreKey ID, inclusive.
    @param count The number of PreKeys to generate.
    @return the list of generated PreKeyRecords.
   """
    @staticmethod
    def generatePreKeys(start, count):
        results = []
        start -= 1
        for i in xrange(0, count):
            results.append(PreKeyRecord(((start + i) % (Medium.MAX_VALUE-1)) + 1, Curve.generateKeyPair()))

        return results


    @staticmethod
    def generateSignedPreKey(identityKeyPair, signedPreKeyId):
        keyPair = Curve.generateKeyPair()
        signature = Curve.calculateSignature(identityKeyPair.getPrivateKey(), keyPair.getPublicKey().serialize())

        #Curve.verifySignature(identityKeyPair.getPublicKey(), keyPair.getPublicKey().serialize(), signature)

        return SignedPreKeyRecord(signedPreKeyId, int(round(time.time() * 1000)), keyPair, signature)

    @staticmethod
    def working_generateSignedPreKey(identityKeyPair, signedPreKeyId):
        pub = "6a04d4b01672d0a69c7a89d69205079a57629856d9351856952fccfe384cff78".decode('hex')
        priv = "".decode('hex')
        keyPair = ECKeyPair(DjbECPublicKey(pub), DjbECPrivateKey(priv))
        signature = "b79755c023839a01322676ccff29f5f27615d56ffbfbcd5162d4fca1ba322d7ddf4e046e133d6fad1c8fda27ce6a0c6d" \
                    "41c30ec83b1655578b88a6351e34340d".decode('hex')

        return SignedPreKeyRecord(signedPreKeyId, int(round(time.time() * 1000)), keyPair, signature)

    @staticmethod
    def _generateSignedPreKey(identityKeyPair, signedPreKeyId):
        keyPair = Curve.generateKeyPair()
        sys.path.append('/home/tarek/testlab/libaxolotl-android/classes.jar')
        sys.path.append('/home/tarek/testlab/libaxolotl-android/protobuf.jar')

        from org.whispersystems.libaxolotl.ecc import Curve

        signature = Curve.calculateSignature(identityKeyPair.getPrivateKey(), keyPair.getPublicKey().serialize())

        return SignedPreKeyRecord(signedPreKeyId, int(round(time.time() * 1000)), keyPair, signature)






