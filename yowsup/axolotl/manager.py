from axolotl.util.keyhelper import KeyHelper
from axolotl.identitykeypair import IdentityKeyPair
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.axolotladdress import AxolotlAddress
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from axolotl.sessionbuilder import SessionBuilder
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.state.prekeybundle import PreKeyBundle
from axolotl.untrustedidentityexception import UntrustedIdentityException
from axolotl.invalidmessageexception import InvalidMessageException
from axolotl.duplicatemessagexception import DuplicateMessageException
from axolotl.invalidkeyidexception import InvalidKeyIdException
from axolotl.nosessionexception import NoSessionException
from axolotl.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage
from axolotl.state.axolotlstore import AxolotlStore
from yowsup.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.axolotl import exceptions
import random
import logging
import sys

logger = logging.getLogger(__name__)


class AxolotlManager(object):

    COUNT_GEN_PREKEYS = 812
    THRESHOLD_REGEN = 10
    MAX_SIGNED_PREKEY_ID = 16777215

    def __init__(self, store, username):
        """
        :param store:
        :type store: AxolotlStore
        :param username:
        :type username: str
        """
        self._username = username # type: str
        self._store = store # type: LiteAxolotlStore
        self._identity = self._store.getIdentityKeyPair() # type: IdentityKeyPair
        self._registration_id = self._store.getLocalRegistrationId() # type: int | None

        assert self._registration_id is not None
        assert self._identity is not None

        self._group_session_builder = GroupSessionBuilder(self._store) # type: GroupSessionBuilder
        self._session_ciphers = {} # type: dict[str, SessionCipher]
        self._group_ciphers = {} # type: dict[str, GroupCipher]
        logger.debug("Initialized AxolotlManager [username=%s, db=%s]" % (self._username, store))

    @property
    def registration_id(self):
        return self._registration_id

    @property
    def identity(self):
        return self._identity

    def level_prekeys(self, force=False):
        logger.debug("level_prekeys(force=%s)" % force)
        pending_prekeys = self._store.loadPreKeys()
        logger.debug("len(pending_prekeys) = %d" % len(pending_prekeys))
        if force or len(pending_prekeys) < self.THRESHOLD_REGEN:
            count_gen = self.COUNT_GEN_PREKEYS - len(pending_prekeys)
            logger.info("Generating %d prekeys" % count_gen)
            prekeys = KeyHelper.generatePreKeys(KeyHelper.getRandomSequence(), count_gen)
            logger.info("Storing %d prekeys" % len(prekeys))
            for i in range(0, len(prekeys)):
                key = prekeys[i]
                if logger.level <= logging.DEBUG:
                    sys.stdout.write("Storing prekey %d/%d \r" % (i + 1, len(prekeys)))
                    sys.stdout.flush()
                self._store.storePreKey(key.getId(), key)
            return prekeys
        return []

    def load_unsent_prekeys(self):
        logger.debug("load_unsent_prekeys")
        unsent = self._store.preKeyStore.loadUnsentPendingPreKeys()
        logger.info("Loaded %d unsent prekeys" % len(unsent))
        return unsent

    def set_prekeys_as_sent(self, prekeyIds):
        """
        :param prekeyIds:
        :type prekeyIds: list
        :return:
        :rtype:
        """
        logger.debug("set_prekeys_as_sent(prekeyIds=[%d prekeyIds])" % len(prekeyIds))
        self._store.preKeyStore.setAsSent([prekey.getId() for prekey in prekeyIds])

    def generate_signed_prekey(self):
        logger.debug("generate_signed_prekey")
        latest_signed_prekey = self.load_latest_signed_prekey(generate=False)
        if latest_signed_prekey is not None:
            if latest_signed_prekey.getId() == self.MAX_SIGNED_PREKEY_ID:
                new_signed_prekey_id = (self.MAX_SIGNED_PREKEY_ID / 2) + 1
            else:
                new_signed_prekey_id = latest_signed_prekey.getId() + 1
        else:
            new_signed_prekey_id = 0
        signed_prekey = KeyHelper.generateSignedPreKey(self._identity, new_signed_prekey_id)
        self._store.storeSignedPreKey(signed_prekey.getId(), signed_prekey)
        return signed_prekey

    def load_latest_signed_prekey(self, generate=False):
        logger.debug("load_latest_signed_prekey")
        signed_prekeys = self._store.loadSignedPreKeys()
        if len(signed_prekeys):
            return signed_prekeys[-1]

        return self.generate_signed_prekey() if generate else None

    def _get_session_cipher(self, recipientid):
        logger.debug("get_session_cipher(recipientid=%s)" % recipientid)
        if recipientid in self._session_ciphers:
            session_cipher = self._session_ciphers[recipientid]
        else:
            session_cipher= SessionCipher(self._store, self._store, self._store, self._store, recipientid, 1)
            self._session_ciphers[recipientid] = session_cipher
        return session_cipher

    def _get_group_cipher(self, groupid, username):
        logger.debug("get_group_cipher(groupid=%s, username=%s)" % (groupid, username))
        senderkeyname = SenderKeyName(groupid, AxolotlAddress(username, 0))
        if senderkeyname in self._group_ciphers:
            group_cipher = self._group_ciphers[senderkeyname]
        else:
            group_cipher = GroupCipher(self._store.senderKeyStore, senderkeyname)
            self._group_ciphers[senderkeyname] = group_cipher
        return group_cipher

    def _generate_random_padding(self):
        logger.debug("generate_random_adding")
        num = random.randint(1,255)
        return bytearray([num] * num)

    def _unpad(self, data):
        padding_byte = data[-1] if type(data[-1]) is int else ord(data[-1]) # bec inconsistent API?
        padding = padding_byte & 0xFF
        return data[:-padding]

    def encrypt(self, recipient_id, message):
        logger.debug("encrypt(recipientid=%s, message=%s)" % (recipient_id, message))
        """
        :param recipient_id:
        :type recipient_id: str
        :param data:
        :type data: bytes
        :return:
        :rtype:
        """
        cipher = self._get_session_cipher(recipient_id)
        return cipher.encrypt(message + self._generate_random_padding())

    def decrypt_pkmsg(self, senderid, data, unpad):
        logger.debug("decrypt_pkmsg(senderid=%s, data=(omitted), unpad=%s)" % (senderid, unpad))
        pkmsg = PreKeyWhisperMessage(serialized=data)
        try:
            plaintext = self._get_session_cipher(senderid).decryptPkmsg(pkmsg)
            return self._unpad(plaintext) if unpad else plaintext
        except NoSessionException:
            raise exceptions.NoSessionException()
        except InvalidKeyIdException:
            raise exceptions.InvalidKeyIdException()
        except InvalidMessageException:
            raise exceptions.InvalidMessageException()
        except DuplicateMessageException:
            raise exceptions.DuplicateMessageException()


    def decrypt_msg(self, senderid, data, unpad):
        logger.debug("decrypt_msg(senderid=%s, data=[omitted], unpad=%s)" % (senderid, unpad))
        msg = WhisperMessage(serialized=data)
        try:
            plaintext = self._get_session_cipher(senderid).decryptMsg(msg)

            return self._unpad(plaintext) if unpad else plaintext
        except NoSessionException:
            raise exceptions.NoSessionException()
        except InvalidKeyIdException:
            raise exceptions.InvalidKeyIdException()
        except InvalidMessageException:
            raise exceptions.InvalidMessageException()
        except DuplicateMessageException:
            raise exceptions.DuplicateMessageException()

    def group_encrypt(self, groupid, message):
        """
        :param groupid:
        :type groupid: str
        :param message:
        :type message: bytes
        :return:
        :rtype:
        """
        logger.debug("group_encrypt(groupid=%s, message=%s)" % (groupid, message))
        group_cipher = self._get_group_cipher(groupid, self._username)
        return group_cipher.encrypt(message + self._generate_random_padding())

    def group_decrypt(self, groupid, participantid, data):
        logger.debug("group_decrypt(groupid=%s, participantid=%s, data=[omitted])" % (groupid, participantid))
        group_cipher = self._get_group_cipher(groupid, participantid)
        try:
            plaintext = group_cipher.decrypt(data)
            plaintext = self._unpad(plaintext)
            return plaintext
        except NoSessionException:
            raise exceptions.NoSessionException()

    def group_create_skmsg(self, groupid):
        logger.debug("group_create_skmsg(groupid=%s)" % groupid)
        senderKeyName = SenderKeyName(groupid, AxolotlAddress(self._username, 0))
        return self._group_session_builder.create(senderKeyName)

    def group_create_session(self, groupid, participantid, skmsgdata):
        """
        :param groupid:
        :type groupid: str
        :param participantid:
        :type participantid: str
        :param skmsgdata:
        :type skmsgdata: bytearray
        :return:
        :rtype:
        """
        logger.debug("group_create_session(groupid=%s, participantid=%s, skmsgdata=[omitted])"
                     % (groupid, participantid))
        senderKeyName = SenderKeyName(groupid, AxolotlAddress(participantid, 0))
        senderkeydistributionmessage = SenderKeyDistributionMessage(serialized=skmsgdata)
        self._group_session_builder.process(senderKeyName, senderkeydistributionmessage)

    def create_session(self, username, prekeybundle, autotrust=False):
        """
        :param username:
        :type username: str
        :param prekeybundle:
        :type prekeybundle: PreKeyBundle
        :return:
        :rtype:
        """
        logger.debug("create_session(username=%s, prekeybunder=[omitted], autotrust=%s)" % (username, autotrust))
        session_builder = SessionBuilder(self._store, self._store, self._store, self._store, username, 1)
        try:
            session_builder.processPreKeyBundle(prekeybundle)
        except UntrustedIdentityException as ex:
            if autotrust:
                self.trust_identity(ex.getName(), ex.getIdentityKey())
            else:
                raise exceptions.UntrustedIdentityException(ex.getName(), ex.getIdentityKey())

    def session_exists(self, username):
        """
        :param username:
        :type username: str
        :return:
        :rtype:
        """
        logger.debug("session_exists(%s)?" % username)
        return self._store.containsSession(username, 1)


    def load_senderkey(self, groupid):
        logger.debug("load_senderkey(groupid=%s)" % groupid)
        senderkeyname = SenderKeyName(groupid, AxolotlAddress(self._username, 0))
        return self._store.loadSenderKey(senderkeyname)

    def trust_identity(self, recipientid, identitykey):
        logger.debug("trust_identity(recipientid=%s, identitykey=[omitted])" % recipientid)
        self._store.saveIdentity(recipientid, identitykey)
