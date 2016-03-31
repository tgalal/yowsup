from yowsup.layers import YowProtocolLayer, YowLayerEvent, EventCallback
from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.layers.network.layer import YowNetworkLayer
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.layers.axolotl.protocolentities import *
from yowsup.structs import ProtocolTreeNode
from yowsup.common.tools import StorageTools
from yowsup.common import YowConstants

from axolotl.sessionbuilder import SessionBuilder
from axolotl.util.keyhelper import KeyHelper
from axolotl.ecc.curve import Curve
from axolotl.protocol.prekeywhispermessage import PreKeyWhisperMessage
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.protocol.senderkeymessage import SenderKeyMessage
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.util.hexutil import HexUtil
from axolotl.invalidmessageexception import InvalidMessageException
from axolotl.duplicatemessagexception import DuplicateMessageException
from axolotl.invalidkeyidexception import InvalidKeyIdException
from axolotl.nosessionexception import NoSessionException
from axolotl.untrustedidentityexception import UntrustedIdentityException
from axolotl.axolotladdress import AxolotlAddress
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder
from axolotl.protocol.senderkeydistributionmessage import SenderKeyDistributionMessage

import binascii
import copy
import sys
import logging

logger = logging.getLogger(__name__)

class YowAxolotlLayer(YowProtocolLayer):
    EVENT_PREKEYS_SET = "org.openwhatsapp.yowsup.events.axololt.setkeys"
    PROP_IDENTITY_AUTOTRUST =  "org.openwhatsapp.yowsup.prop.axolotl.INDENTITY_AUTOTRUST"
    _STATE_INIT = 0
    _STATE_GENKEYS = 1
    _STATE_HASKEYS = 2
    _COUNT_PREKEYS = 200
    _DB = "axolotl.db"

    def __init__(self):
        super(YowAxolotlLayer, self).__init__()
        self.store = None
        self.state = self.__class__._STATE_INIT

        self.sessionCiphers = {}
        self.groupCiphers = {}
        self.pendingMessages = {}
        self.pendingIncomingMessages = {}
        self.skipEncJids = []
        self.v2Jids = [] #people we're going to send v2 enc messages
        self.retryIncomingMessages = {}

    @property
    def store(self):
        if self._store is None:
            self.store = LiteAxolotlStore(
                StorageTools.constructPath(
                    self.getProp(
                        YowAuthenticationProtocolLayer.PROP_CREDENTIALS)[0],
                    self.__class__._DB
                )
            )
            self.state = self.__class__._STATE_HASKEYS if  self.store.getLocalRegistrationId() is not None \
                else self.__class__._STATE_INIT

        return self._store

    @store.setter
    def store(self, store):
        self._store = store

    def __str__(self):
        return "Axolotl Layer"

    ### store and state


    def isInitState(self):
        return self.store == None or self.state == self.__class__._STATE_INIT

    def isGenKeysState(self):
        return self.state == self.__class__._STATE_GENKEYS
    ########


    @EventCallback(EVENT_PREKEYS_SET)
    def onPreKeysSet(self, yowLayerEvent):
        self.sendKeys(fresh=False)

    @EventCallback(YowNetworkLayer.EVENT_STATE_CONNECTED)
    def onConnected(self, yowLayerEvent):
        if self.isInitState():
            self.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, True)

    @EventCallback(YowAuthenticationProtocolLayer.EVENT_AUTHED)
    def onAuthed(self, yowLayerEvent):
        if yowLayerEvent.getArg("passive") and self.isInitState():
            logger.info("Axolotl layer is generating keys")
            self.sendKeys()

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onDisconnected(self, yowLayerEvent):
        if self.isGenKeysState():
            #we requested this disconnect in this layer to switch off passive
            #no need to traverse it to upper layers?
            self.setProp(YowAuthenticationProtocolLayer.PROP_PASSIVE, False)
            self.state = self.__class__._STATE_HASKEYS
            self.getLayerInterface(YowNetworkLayer).connect()
        else:
            self.store = None

    def send(self, node):
        if node.tag == "message" and node["to"] not in self.skipEncJids and not YowConstants.WHATSAPP_GROUP_SERVER in node["to"] and not YowConstants.WHATSAPP_BROADCAST_SERVER in node["to"]:
            self.handlePlaintextNode(node)
            return
        self.toLower(node)

    def receive(self, protocolTreeNode):
        """
        :type protocolTreeNode: ProtocolTreeNode
        """
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "message" or protocolTreeNode.tag == "media":
                self.onMessage(protocolTreeNode)
                return
            elif protocolTreeNode.tag == "notification" and protocolTreeNode["type"] == "encrypt":
                self.onEncryptNotification(protocolTreeNode)
                return
            elif protocolTreeNode.tag == "receipt" and protocolTreeNode["type"] == "retry":
                # should bring up that message, resend it, but in upper layer?
                # as it might have to be fetched from a persistent storage
                pass
            self.toUpper(protocolTreeNode)
    ######

    ##### handling received data #####
    def onEncryptNotification(self, protocolTreeNode):
        entity = EncryptNotification.fromProtocolTreeNode(protocolTreeNode)
        ack = OutgoingAckProtocolEntity(protocolTreeNode["id"], "notification", protocolTreeNode["type"], protocolTreeNode["from"])
        self.toLower(ack.toProtocolTreeNode())
        self.sendKeys(fresh=False, countPreKeys = self.__class__._COUNT_PREKEYS - entity.getCount())

    def onMessage(self, protocolTreeNode):
        encNode = protocolTreeNode.getChild("enc")
        if encNode:
            self.handleEncMessage(protocolTreeNode)
        else:
            self.toUpper(protocolTreeNode)

    ####

    def processPendingMessages(self, jid):
        if jid in self.pendingMessages:
            for messageNode in self.pendingMessages[jid]:
                if jid in self.skipEncJids:
                    self.toLower(messageNode)
                else:
                    self.handlePlaintextNode(messageNode)

            del self.pendingMessages[jid]

    def processPendingIncomingMessages(self, jid):
        if jid in self.pendingIncomingMessages:
            for messageNode in self.pendingIncomingMessages[jid]:
                self.onMessage(messageNode)

            del self.pendingIncomingMessages[jid]

    #### handling message types

    def handlePlaintextNode(self, node):
        recipient_id = node["to"].split('@')[0]
        v2 = node["to"] in self.v2Jids
        if not self.store.containsSession(recipient_id, 1):
            entity = GetKeysIqProtocolEntity([node["to"]])
            if node["to"] not in self.pendingMessages:
                self.pendingMessages[node["to"]] = []
            self.pendingMessages[node["to"]].append(node)

            self._sendIq(entity, lambda a, b: self.onGetKeysResult(a, b, self.processPendingMessages), self.onGetKeysError)
        elif v2 or not node.getChild("media"): #media enc is only for v2 messsages
            messageData = self.serializeToProtobuf(node) if v2 else node.getChild("body").getData()
            if messageData:
                sessionCipher = self.getSessionCipher(recipient_id)
                ciphertext = sessionCipher.encrypt(messageData)

                mediaType = node.getChild("media")["type"] if node.getChild("media") else None

                encEntity = EncryptedMessageProtocolEntity(
                [
                    EncProtocolEntity(EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG ,
                                                   2 if v2 else 1,
                                                   ciphertext.serialize(), mediaType)],
                                                   "text" if not mediaType else "media",
                                                   _id= node["id"],
                                                   to = node["to"],
                                                   notify = node["notify"],
                                                   timestamp= node["timestamp"],
                                                   participant=node["participant"],
                                                   offline=node["offline"],
                                                   retry=node["retry"]
                                                   )
                self.toLower(encEntity.toProtocolTreeNode())
            else: #case of unserializable messages (audio, video) ?
                self.toLower(node)
        else:
            self.toLower(node)

    def handleEncMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        isGroup =  node["participant"] is not None
        senderJid = node["participant"] if isGroup else node["from"]
        encNode = None
        if node.getChild("enc")["v"] == "2" and senderJid not in self.v2Jids:
            self.v2Jids.append(senderJid)
        try:
            if encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG):
                self.handlePreKeyWhisperMessage(node)
            elif encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG):
                self.handleWhisperMessage(node)
            elif encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG):
                self.handleSenderKeyMessage(node)

            if node["id"] in self.retryIncomingMessages:
                del self.retryIncomingMessages[node["id"]]

        except NoSessionException as e:
            logger.error(e)
            entity = GetKeysIqProtocolEntity([senderJid])
            if senderJid not in self.pendingIncomingMessages:
                self.pendingIncomingMessages[senderJid] = []
            self.pendingIncomingMessages[senderJid].append(node)

            self._sendIq(entity, lambda a, b: self.onGetKeysResult(a, b, self.processPendingIncomingMessages), self.onGetKeysError)
        except DuplicateMessageException as e:
            logger.error(e)
            logger.warning("Going to send the delivery receipt myself !")
            self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"], read=False, participant = node["participant"], t=node["t"]).toProtocolTreeNode())

        except UntrustedIdentityException as e:
            if(self.getProp(self.__class__.PROP_IDENTITY_AUTOTRUST, False)):
                logger.warning("Autotrusting identity for %s" % e.getName())
                self.store.saveIdentity(e.getName(), e.getIdentityKey())
                return self.handleEncMessage(node)
            else:
                logger.error(e)
                logger.warning("Ignoring message with untrusted identity")
        except (InvalidMessageException, InvalidKeyIdException, Exception) as e:
            logger.warning(e)
            self.retryIncomingMessages[node["id"]] = (self.retryIncomingMessages[node["id"]] + 1) if node["id"] in self.retryIncomingMessages else 1
            if self.retryIncomingMessages[node["id"]] > 5:
                 logger.warning("Too many retries!! Going to send the delivery receipt myself!")
                 self.toLower(OutgoingReceiptProtocolEntity(node["id"], node["from"], read=False, participant = node["participant"], t=node["t"]).toProtocolTreeNode())
            else:
                 retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
                 retry.setRegData(self.store.getLocalRegistrationId())
                 self.toLower(retry.toProtocolTreeNode())

    def handlePreKeyWhisperMessage(self, node):
        pkMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = pkMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_PKMSG)
        preKeyWhisperMessage = PreKeyWhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(pkMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptPkmsg(preKeyWhisperMessage)
        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(pkMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(node, plaintext)

    def handleWhisperMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)

        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_MSG)
        whisperMessage = WhisperMessage(serialized=enc.getData())
        sessionCipher = self.getSessionCipher(encMessageProtocolEntity.getAuthor(False))
        plaintext = sessionCipher.decryptMsg(whisperMessage)

        if enc.getVersion() == 2:
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext[:-padding])
        else:
            self.handleConversationMessage(encMessageProtocolEntity.toProtocolTreeNode(), plaintext)

    def handleSenderKeyMessage(self, node):
        encMessageProtocolEntity = EncryptedMessageProtocolEntity.fromProtocolTreeNode(node)
        enc = encMessageProtocolEntity.getEnc(EncProtocolEntity.TYPE_SKMSG)

        senderKeyName = SenderKeyName(encMessageProtocolEntity.getFrom(True), AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 0))
        groupCipher = GroupCipher(self.store, senderKeyName)
        try:
            plaintext = groupCipher.decrypt(enc.getData())
            padding = ord(plaintext[-1]) & 0xFF
            self.parseAndHandleMessageProto(encMessageProtocolEntity, plaintext[:-padding])
        except NoSessionException as e:
            logger.error(e)
            retry = RetryOutgoingReceiptProtocolEntity.fromMessageNode(node)
            retry.setRegData(self.store.getLocalRegistrationId())
            self.toLower(retry.toProtocolTreeNode())

    def parseAndHandleMessageProto(self, encMessageProtocolEntity, serializedData):
        node = encMessageProtocolEntity.toProtocolTreeNode()
        m = Message()
        try:
            m.ParseFromString(serializedData)
        except:
            print("DUMP:")
            #with open("/tmp/protobuf.bin", "wb") as f:
            #    f.write(serializedData)
            print(serializedData)
            print([s for s in serializedData])
            print([ord(s) for s in serializedData])
            raise
        if not m or not serializedData:
            raise ValueError("Empty message")

        if m.HasField("sender_key_distribution_message"):
            axolotlAddress = AxolotlAddress(encMessageProtocolEntity.getParticipant(False), 0)
            self.handleSenderKeyDistributionMessage(m.sender_key_distribution_message, axolotlAddress)

        if m.HasField("conversation"):
            self.handleConversationMessage(node, m.conversation)
        elif m.HasField("contact_message"):
            self.handleContactMessage(node, m.contact_message)
        elif m.HasField("url_message"):
            self.handleUrlMessage(node, m.url_message)
        elif m.HasField("location_message"):
            self.handleLocationMessage(node, m.location_message)
        elif m.HasField("image_message"):
            self.handleImageMessage(node, m.image_message)
        elif m.HasField("document_message"):
            self.handleDocumentMessage(node, m.document_message)
        elif m.HasField("video_message"):
            self.handleVideoMessage(node, m.video_message)
        elif m.HasField("audio_message"):
            self.handleAudioMessage(node, m.audio_message)
        else:
            print(m)
            raise ValueError("Unhandled")

    def handleSenderKeyDistributionMessage(self, senderKeyDistributionMessage, axolotlAddress):
        groupId = senderKeyDistributionMessage.groupId
        axolotlSenderKeyDistributionMessage = SenderKeyDistributionMessage(serialized=senderKeyDistributionMessage.axolotl_sender_key_distribution_message)
        groupSessionBuilder = GroupSessionBuilder(self.store)
        senderKeyName = SenderKeyName(groupId, axolotlAddress)
        groupSessionBuilder.process(senderKeyName, axolotlSenderKeyDistributionMessage)

    def handleConversationMessage(self, originalEncNode, text):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode.children = []
        messageNode.addChild(ProtocolTreeNode("body", data = text))
        self.toUpper(messageNode)

    def handleImageMessage(self, originalEncNode, imageMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "image",
            "filehash": imageMessage.file_sha256,
            "size": str(imageMessage.file_length),
            "url": imageMessage.url,
            "mimetype": imageMessage.mime_type,
            "width": str(imageMessage.width),
            "height": str(imageMessage.height),
            "caption": imageMessage.caption,
            "encoding": "raw",
            "file": "enc",
            "ip": "0",
            "mediakey": imageMessage.media_key
        }, data = imageMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleAudioMessage(self, originalEncNode, audioMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "audio",
            "filehash": audioMessage.file_sha256,
            "size": str(audioMessage.file_length),
            "url": audioMessage.url,
            "mimetype": audioMessage.mime_type,
            "duration": str(audioMessage.duration),
            "seconds": str(audioMessage.duration),
            "encoding": "raw",
            "file": "enc",
            "ip": "0",
            "mediakey": audioMessage.media_key
        })
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleVideoMessage(self, originalEncNode, videoMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "video",
            "filehash": videoMessage.file_sha256,
            "size": str(videoMessage.file_length),
            "url": videoMessage.url,
            "mimetype": videoMessage.mime_type,
            "duration": str(videoMessage.duration),
            "seconds": str(videoMessage.duration),
            "caption": videoMessage.caption,
            "encoding": "raw",
            "file": "enc",
            "ip": "0",
            "mediakey": videoMessage.media_key
        }, data = videoMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleUrlMessage(self, originalEncNode, urlMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "url",
            "text": urlMessage.text,
            "match": urlMessage.matched_text,
            "url": urlMessage.canonical_url,
            "description": urlMessage.description,
            "title": urlMessage.title
        }, data = urlMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleDocumentMessage(self, originalEncNode, documentMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "document",
            "url": documentMessage.url,
            "mimetype": documentMessage.mime_type,
            "title": documentMessage.title,
            "filehash": documentMessage.file_sha256,
            "size": str(documentMessage.file_length),
            "pages": str(documentMessage.page_count),
            "mediakey": documentMessage.media_key
        }, data = documentMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)

        self.toUpper(messageNode)

    def handleLocationMessage(self, originalEncNode, locationMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "latitude": str(locationMessage.degrees_latitude),
            "longitude": str(locationMessage.degrees_longitude),
            "name": "%s %s" % (locationMessage.name, locationMessage.address),
            "url": locationMessage.url,
            "encoding": "raw",
            "type": "location"
        }, data=locationMessage.jpeg_thumbnail)
        messageNode.addChild(mediaNode)
        self.toUpper(messageNode)

    def handleContactMessage(self, originalEncNode, contactMessage):
        messageNode = copy.deepcopy(originalEncNode)
        messageNode["type"] = "media"
        mediaNode = ProtocolTreeNode("media", {
            "type": "vcard"
        }, [
            ProtocolTreeNode("vcard", {"name": contactMessage.display_name}, data = contactMessage.vcard)
        ] )
        messageNode.addChild(mediaNode)
        self.toUpper(messageNode)

    def decodeInt7bit(self, string):
        idx = 0
        while ord(string[idx]) >= 128:
            idx += 1
        consumedBytes = idx + 1
        value = 0
        while idx >= 0:
            value <<= 7
            value += ord(string[idx]) % 128
            idx -= 1
        return value, consumedBytes

    def unpadV2Plaintext(self, v2plaintext):
        end = -ord(v2plaintext[-1]) # length of the left padding
        length,consumed = self.decodeInt7bit(v2plaintext[1:])
        return v2plaintext[1+consumed:end]

    def serializeToProtobuf(self, node):
        if node.getChild("body"):
            return self.serializeTextToProtobuf(node)
        elif node.getChild("media"):
            return self.serializeMediaToProtobuf(node.getChild("media"))
        else:
            raise ValueError("No body or media nodes found")

    def serializeTextToProtobuf(self, node):
        m = Message()
        m.conversation = node.getChild("body").getData()
        # Whatsapp encoding needs a terminal 1 byte
        return m.SerializeToString() + '\01'

    def serializeMediaToProtobuf(self, mediaNode):
        if mediaNode["type"] == "image":
            return self.serializeImageToProtobuf(mediaNode)
        if mediaNode["type"] == "location":
            return self.serializeLocationToProtobuf(mediaNode)
        if mediaNode["type"] == "vcard":
            return self.serializeContactToProtobuf(mediaNode)

        return None

    def serializeLocationToProtobuf(self, mediaNode):
        m = Message()
        location_message = LocationMessage()
        location_message.degress_latitude = float(mediaNode["latitude"])
        location_message.degress_longitude = float(mediaNode["longitude"])
        location_message.address = mediaNode["name"]
        location_message.name = mediaNode["name"]
        location_message.url = mediaNode["url"]

        m.location_message.MergeFrom(location_message)
        return m.SerializeToString()

    def serializeContactToProtobuf(self, mediaNode):
        vcardNode = mediaNode.getChild("vcard")
        m = Message()
        contact_message = ContactMessage()
        contact_message.display_name = vcardNode["name"]
        m.vcard = vcardNode.getData()
        m.contact_message.MergeFrom(contact_message)

        return m.SerializeToString()

    def serializeImageToProtobuf(self, mediaNode):
        m = Message()
        image_message = ImageMessage()
        image_message.url = mediaNode["url"]
        image_message.width = int(mediaNode["width"])
        image_message.height = int(mediaNode["height"])
        image_message.mime_type = mediaNode["mimetype"]
        image_message.file_sha256 = mediaNode["filehash"]
        image_message.file_length = int(mediaNode["size"])
        image_message.caption = mediaNode["caption"] or ""
        image_message.jpeg_thumbnail = mediaNode.getData()

        m.image_message.MergeFrom(image_message)
        return m.SerializeToString()

    def serializeUrlToProtobuf(self, node):
        pass

    def serializeDocumentToProtobuf(self, node):
        pass

    ### keys set and get
    def sendKeys(self, fresh = True, countPreKeys = _COUNT_PREKEYS):
        identityKeyPair     = KeyHelper.generateIdentityKeyPair() if fresh else self.store.getIdentityKeyPair()
        registrationId      = KeyHelper.generateRegistrationId() if fresh else self.store.getLocalRegistrationId()
        preKeys             = KeyHelper.generatePreKeys(KeyHelper.getRandomSequence(), countPreKeys)
        signedPreKey        = KeyHelper.generateSignedPreKey(identityKeyPair, KeyHelper.getRandomSequence(65536))
        preKeysDict = {}
        for preKey in preKeys:
            keyPair = preKey.getKeyPair()
            preKeysDict[self.adjustId(preKey.getId())] = self.adjustArray(keyPair.getPublicKey().serialize()[1:])

        signedKeyTuple = (self.adjustId(signedPreKey.getId()),
                          self.adjustArray(signedPreKey.getKeyPair().getPublicKey().serialize()[1:]),
                          self.adjustArray(signedPreKey.getSignature()))

        setKeysIq = SetKeysIqProtocolEntity(self.adjustArray(identityKeyPair.getPublicKey().serialize()[1:]), signedKeyTuple, preKeysDict, Curve.DJB_TYPE, self.adjustId(registrationId))

        onResult = lambda _, __: self.persistKeys(registrationId, identityKeyPair, preKeys, signedPreKey, fresh)
        self._sendIq(setKeysIq, onResult, self.onSentKeysError)

    def persistKeys(self, registrationId, identityKeyPair, preKeys, signedPreKey, fresh):
        total = len(preKeys)
        curr = 0
        prevPercentage = 0

        if fresh:
            self.store.storeLocalData(registrationId, identityKeyPair)
        self.store.storeSignedPreKey(signedPreKey.getId(), signedPreKey)

        for preKey in preKeys:
            self.store.storePreKey(preKey.getId(), preKey)
            curr += 1
            currPercentage = int((curr * 100) / total)
            if currPercentage == prevPercentage:
                continue
            prevPercentage = currPercentage
            #logger.debug("%s" % currPercentage + "%")
            sys.stdout.write("Storing prekeys %d%% \r" % (currPercentage))
            sys.stdout.flush()

        if fresh:
            self.state = self.__class__._STATE_GENKEYS
            self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))

    def onSentKeysError(self, errorNode, keysEntity):
        raise Exception("Sent keys were not accepted")

    def onGetKeysResult(self, resultNode, getKeysEntity, processPendingFn):
        entity = ResultGetKeysIqProtocolEntity.fromProtocolTreeNode(resultNode)

        resultJids = entity.getJids()
        for jid in getKeysEntity.getJids():

            if jid not in resultJids:
                self.skipEncJids.append(jid)
                self.processPendingMessages(jid)
                continue

            recipient_id = jid.split('@')[0]
            preKeyBundle = entity.getPreKeyBundleFor(jid)

            sessionBuilder = SessionBuilder(self.store, self.store, self.store,
                                               self.store, recipient_id, 1)
            sessionBuilder.processPreKeyBundle(preKeyBundle)

            processPendingFn(jid)

    def onGetKeysError(self, errorNode, getKeysEntity):
        pass
    ###

    def adjustArray(self, arr):
        return HexUtil.decodeHex(binascii.hexlify(arr))

    def adjustId(self, _id):
        _id = format(_id, 'x')
        zfiller = len(_id) if len(_id) % 2 == 0 else len(_id) + 1
        _id = _id.zfill(zfiller if zfiller > 6 else 6)
        # if len(_id) % 2:
        #     _id = "0" + _id
        return binascii.unhexlify(_id)

    def getSessionCipher(self, recipientId):
        if recipientId in self.sessionCiphers:
            sessionCipher = self.sessionCiphers[recipientId]
        else:
            sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            self.sessionCiphers[recipientId] = sessionCipher

        return sessionCipher

    def getGroupCipher(self, groupId, senderId):
        senderKeyName = SenderKeyName(groupId, AxolotlAddress(senderId, 1))
        if senderKeyName in self.groupCiphers:
            groupCipher = self.groupCiphers[senderKeyName]
        else:
            groupCipher = GroupCipher(self.store, senderKeyName)
            self.groupCiphers[senderKeyName] = groupCipher
        return groupCipher
