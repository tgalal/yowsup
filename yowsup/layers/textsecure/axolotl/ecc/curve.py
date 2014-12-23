import curve25519
import os
import ctypes

from djbec import DjbECPrivateKey, DjbECPublicKey
from eckeypair import ECKeyPair

#/home/tarek/Projects/yowsup/libs/x86_64/libcurve25519.so
PATH_LIB_CURVE = "/mnt/XPlatform/Projects/python-axolotl/build/lib.linux-x86_64-2.7/curve25519.so"

ctypes.cdll.LoadLibrary(PATH_LIB_CURVE)
_curve = ctypes.CDLL(PATH_LIB_CURVE)


class Curve:

    DJB_TYPE = 5

    # always DJB curve25519 keys
    @staticmethod
    def generateKeyPair():
        privateKey = curve25519.keys.Private()
        publicKey = privateKey.get_public()
        return ECKeyPair(DjbECPublicKey(publicKey.public), DjbECPrivateKey(privateKey.private))

    @staticmethod
    def decodePoint(bytes, offset=0):
        type = bytes[0] # byte appears to be automatically converted to an integer??

        if type == Curve.DJB_TYPE:
            type = bytes[offset] & 0xFF
            if type != Curve.DJB_TYPE:
                raise Exception("InvalidKeyException Unknown key type: " + str(type) )
            keyBytes = bytes[offset+1:][:32]
            return DjbECPublicKey(str(keyBytes))
        else:
            raise Exception("InvalidKeyException Unknown key type: " + str(type) )

    @staticmethod
    def decodePrivatePoint(bytes):
        return DjbECPrivateKey(str(bytes))


    @staticmethod
    def calculateAgreement(publicKey, privateKey):
        out = ctypes.c_char_p(str(bytearray(32)))
        _curve.curve25519_donna(out, privateKey.getPrivateKey(), publicKey.getPublicKey())
        return out.value

    @staticmethod
    def xcalculateAgreement(publicKey, privateKey):
        #key = curve25519.keys.Private(secret=privateKey)
        #return key.get_shared_key(curve25519.keys.Public(publicKey), lambda x: x)
        secret = ''.join(privateKey.getPrivateKey()) #because for some reason keysPrivate changes 1st byte of secret to 32
        key = curve25519.keys.Private(secret = secret)
        publicKey = publicKey.getPublicKey()
        l = len(publicKey)
        return key.get_shared_key(curve25519.keys.Public(publicKey), lambda  x: x)

    @staticmethod
    def verifySignature(ecPublicSigningKey, message, signature):
        result = _curve.curve25519_verify(signature, ecPublicSigningKey.getPublicKey(), message, len(message))
        return result == 0
        # pk = ecPublicSigningKey.serialize()
        #return ed.checkvalid(signature, message, ecPublicSigningKey.serialize()[1:])
        #return ed2.checkvalid(signature, message, ecPublicSigningKey.serialize()[1:])
        # raise Exception("IMPL ME")

    _CALC_ATTEMPTS  = 0
    @staticmethod
    def calculateSignature(ecPrivateSigningKey, message):
        rand = os.urandom(64)
        out = ctypes.c_char_p('')
        res = _curve.curve25519_sign(out, ecPrivateSigningKey.getPrivateKey(), message, len(message), rand)

        if len(out.value) != 64:
            if Curve._CALC_ATTEMPTS > 20:
                raise AssertionError("Couldn't generate a valid signature !!")
            Curve._CALC_ATTEMPTS += 1
            return Curve.calculateSignature(ecPrivateSigningKey, message)
        Curve._CALC_ATTEMPTS = 0
        return out.value
        #return _curve.curve25519_sign()
        #signature =  ed.signature(message, ecPrivateSigningKey.serialize(), rand)
        #return signature
        #signingKey = ed25519.SigningKey(ecPrivateSigningKey.serialize())
        #return signingKey.sign(message)
