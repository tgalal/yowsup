import os
import struct

from yowsup.layers import YowLayer
from protocolentities import SetKeysIqProtocolEntity
from axolotl.util.keyhelper import KeyHelper

#from pytextsecure import ratcheting_session
import binascii

import sys


class YowTextSecureLayer(YowLayer):
    EVENT_PREKEYS_SET = "org.openwhatsapp.yowsup.events.textsecure.set"
    TYPE_DJB = 0x5
    def __init__(self):
        super(YowTextSecureLayer, self).__init__()

    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        self.toUpper(data)

    def onEvent(self, yowLayerEvent):
        if yowLayerEvent.getName() == self.__class__.EVENT_PREKEYS_SET:
            #self.jypysendKeys()
            self.ownJySendKeys()

    def adjustArray(self, arr):
        return binascii.hexlify(arr).decode('hex')
        #return "".join(map(chr,list(bytearray(arr))))
        #return list(arr)

    def adjustId(self, _id):
        _id = format(_id, 'x').zfill(6)
        # if len(_id) % 2:
        #     _id = "0" + _id
        return binascii.unhexlify(_id)


    # def sendKeys(self, dummy = None):
    #     database = "/home/tarek/Projects/yowsup/stuff/axolotl.db"
    #     conn = sqlite3.connect(database)
    #     c = conn.cursor()
    #     c.execute("select prekey_id, record from prekeys")
    #     row = c.fetchone()
    #     prekey_id, record = row
    #     print prekey_id
    #     print record


    def ownJySendKeys(self, dummy = None):
        sys.path.append('/home/tarek/testlab/libaxolotl-android/classes.jar')
        sys.path.append('/home/tarek/testlab/libaxolotl-android/protobuf.jar')
        identityKeyPair     = KeyHelper.generateIdentityKeyPair()
        registrationId      = KeyHelper.generateRegistrationId()
        preKeys             = KeyHelper.generatePreKeys(7493876, 200)
        signedPreKey        = KeyHelper.generateSignedPreKey(identityKeyPair, 0)

        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
           # strKeyId = str(preKey.getId())
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))



        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))
        setKeysIq.log()
        self.toLower(setKeysIq.toProtocolTreeNode())



    def jysendKeys(self, dummy = None):
        sys.path.append('/home/tarek/testlab/libaxolotl-android/classes.jar')
        sys.path.append('/home/tarek/testlab/libaxolotl-android/protobuf.jar')
        from org.whispersystems.libaxolotl.util import KeyHelper
        identityKeyPair = KeyHelper.generateIdentityKeyPair()
        registrationId  = KeyHelper.generateRegistrationId(True)
        preKeys         = KeyHelper.generatePreKeys(7493876, 200)
        signedPreKey    = KeyHelper.generateSignedPreKey(identityKeyPair, 0)
        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
           # strKeyId = str(preKey.getId())
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))



        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))
        setKeysIq.log()
        self.toLower(setKeysIq.toProtocolTreeNode())



    def jypysendKeys(self, dummy = None):
        sys.path.append('/home/tarek/testlab/libaxolotl-android/classes.jar')
        sys.path.append('/home/tarek/testlab/libaxolotl-android/protobuf.jar')
        from org.whispersystems.libaxolotl.util import KeyHelper
        '''
            NEXT:
            MAKE KEYS WORK IN PYTHON
            TO USE ALREADY IMPLEMENTED SESSION FROM pytextsecure
        '''
        identityKeyPair = KeyHelper.generateIdentityKeyPair()
        signedPreKey = KeyHelper.generateSignedPreKey(identityKeyPair, 0)
        #from curve25519 import keys
        import keyutils



        identityKeyPair = keyutils.genKey()
        registrationId = abs(struct.unpack('>i', bytearray(os.urandom(4)))[0])#int(binascii.hexlify(bytearray(os.urandom(4))), 16)#437332805
        preKeysDict = {}
        preKeyUtils = keyutils.PreKeyUtil()
        preKeyUtils.generatePreKeys()
        for preKey in preKeyUtils.getPreKeys():
            preKeysDict[self.adjustId(preKey.keyId)] = self.adjustArray(preKey.publicKey)

        #signedPreKey = preKeyUtils.generateSignedPreKey(identityKeyPair[0])

        '''
        ECKeyPair keyPair   = Curve.generateKeyPair();
        byte[]    signature = Curve.calculateSignature(identityKeyPair.getPrivateKey(), keyPair.getPublicKey().serialize());

        return new SignedPreKeyRecord(signedPreKeyId, System.currentTimeMillis(), keyPair, signature);
        '''


        #signedKeyTuple = (self.adjustId(0),
        #    self.adjustArray(signedPreKey[1][1]),
        #    self.adjustArray(signedPreKey[0])
        #)


        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                  self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                  self.adjustArray(signedPreKey.getSignature()))
        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))

        self.toLower(setKeysIq.toProtocolTreeNode())
    def pysendKeys(self, dummy = None):
        '''
            NEXT:
            MAKE KEYS WORK IN PYTHON
            TO USE ALREADY IMPLEMENTED SESSION FROM pytextsecure
        '''
        from pytextsecure import keyutils, database, dbmodel

        db_path = "/home/tarek/yowdebug/config.db"
        newDb = not os.path.exists(db_path)

        tsb = database.TextSecureDatabase("sqlite:///%s" % db_path)
        tsb.init_db(dbmodel.Base)
        identityKeyPair = keyutils.genKey()
        registrationId = abs(struct.unpack('>i', bytearray(os.urandom(4)))[0])#int(binascii.hexlify(bytearray(os.urandom(4))), 16)#437332805
        preKeysDict = {}
        preKeyUtils = keyutils.PreKeyUtil()
        preKeyUtils.generatePreKeys()
        for preKey in preKeyUtils.getPreKeys():
            preKeysDict[self.adjustId(preKey.keyId)] = self.adjustArray(preKey.publicKey)

        signedPreKey = preKeyUtils.generateSignedPreKey(identityKeyPair[0])

        '''
        ECKeyPair keyPair   = Curve.generateKeyPair();
        byte[]    signature = Curve.calculateSignature(identityKeyPair.getPrivateKey(), keyPair.getPublicKey().serialize());

        return new SignedPreKeyRecord(signedPreKeyId, System.currentTimeMillis(), keyPair, signature);
        '''


        signedKeyTuple = (self.adjustId(0),
            self.adjustArray(signedPreKey[1][1]),
            self.adjustArray(signedPreKey[0])
        )
        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair[1]), signedKeyTuple, preKeysDict, self.__class__.TYPE_DJB, self.adjustId(registrationId))

        self.toLower(setKeysIq.toProtocolTreeNode())



    def _sendKeys(self):
        _privateKey = keys.Private()
        privateKey = _privateKey.serialize()
        publicKey = _privateKey.get_public().serialize()
        preKeysDict = {}
        for i in xrange(0, 200):
            prekey_id = binascii.hexlify(hex(0x100000 + i))
            preKeysDict[prekey_id] = publicKey

    def __sendKeys(self):
        db_path = "/home/tarek/config.db"
        newDb = not os.path.exists(db_path)

        tsb = database.TextSecureDatabase("sqlite:///%s" % db_path)
        tsb.init_db(dbmodel.Base)
        pku = keyutils.PreKeyUtil()
        identityu = keyutils.IdentityKeyUtil()
        if True:
            pku.generatePreKeys()
            identityu.generateIdentityKey()

            preKeys = pku.getPreKeys()
            preKeysDict = {}
            for preKey in preKeys:
                strKeyId = str(preKey.keyId)
                if len(strKeyId) % 2:
                    strKeyId = "0" + strKeyId
                preKeysDict[strKeyId.decode('hex')] = preKey.publicKey

            #signedkey = ("000000".decode("hex"), preKeys[0].publicKey, "abc")
            #signedKey = pku.generateSignedPreKey(identityu.getIdentityPrivKey())
            #signedkeyTuple = ("000000".decode("hex"), signedKey[1][0], signedKey[0])
            #keyPair = keyutils.genKey()
            keyPair = ratcheting_session.Curve().generateKeyPair()
            print keyPair.publicKey.serialize()
            signature = ratcheting_session.Curve().calculateAgreement(identityu.getIdentityPrivKey(), keyPair.publicKey.serialize())
            signedkeyTuple = ("000000".decode("hex"), keyPair.privateKey.serialize(), signature)

            setKeysIq = SetKeysIqProtocolEntity(identityu.getIdentityKey(), signedkeyTuple, preKeysDict, self.__class__.TYPE_DJB)
            self.toLower(setKeysIq.toProtocolTreeNode())
            print(setKeysIq.toProtocolTreeNode())

