from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.protocol_messages.proto.wa_pb2 import SenderKeyDistributionMessage as ProtoSenderKeyDistributionMessage
from yowsup.layers.axolotl.protocolentities import *
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.protocol_groups.protocolentities import InfoGroupsIqProtocolEntity, InfoGroupsResultIqProtocolEntity
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.axolotladdress import AxolotlAddress
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.groups.senderkeyname import SenderKeyName
from axolotl.groups.groupsessionbuilder import GroupSessionBuilder

import logging
from random import randint

from .layer_base import AxolotlBaseLayer

logger = logging.getLogger(__name__)

class AxolotlSendLayer(AxolotlBaseLayer):
    MAX_SENT_QUEUE = 100
    def __init__(self):
        super(AxolotlSendLayer, self).__init__()

        self.sessionCiphers = {}
        self.groupSessionBuilder = None
        self.groupCiphers = {}
        '''
            Sent messages will be put in skalti entQueue until we receive a receipt for them.
            This is for handling retry receipts which requires re-encrypting and resend of the original message
            As the receipt for a sent message might arrive at a different yowsup instance,
            ideally the original message should be fetched from a persistent storage.
            Therefore, if the original message is not in sentQueue for any reason, we will
            notify the upper layers and let them handle it.
        '''
        self.sentQueue = []

    def onNewStoreSet(self, store):
        if store is not None:
            self.groupSessionBuilder = GroupSessionBuilder(store)

    def __str__(self):
        return "Axolotl Layer"


    def send(self, node):
        if node.tag == "message" and node["to"] not in self.skipEncJids and not node.getChild("enc") and (not node.getChild("media") or node.getChild("media")["mediakey"]):
            self.processPlaintextNodeAndSend(node)
        # elif node.tag == "iq" and node["xmlns"] == "w:m":
        #     mediaNode = node.getChild("media")
        #     if mediaNode and mediaNode["type"] == "image":
        #         iqNode = IqProtocolEntity.fromProtocolTreeNode(node).toProtocolTreeNode()
        #         iqNode.addChild(ProtocolTreeNode(
        #             "encr_media", {
        #                 "type": mediaNode["type"],
        #                 "hash": mediaNode["hash"]
        #             }
        #         ))
        #         self.toLower(iqNode)
        else:
            self.toLower(node)

    def receive(self, protocolTreeNode):
        if not self.processIqRegistry(protocolTreeNode):
            if protocolTreeNode.tag == "receipt":
                messageNode = self.getEnqueuedMessageNode(protocolTreeNode["id"])
                if not messageNode:
                    logger.debug("Axolotl layer does not have the message, bubbling it upwards")
                    self.toUpper(protocolTreeNode)
                elif protocolTreeNode["type"] == "retry":
                    print("retrying")
                    print(protocolTreeNode)
                    logger.info("Got retry to for message %s, and Axolotl layer has the message" % protocolTreeNode["id"])
                    self.getKeysFor([protocolTreeNode["from"]], lambda: self.processPlaintextNodeAndSend(messageNode))
                else:
                    #not interested in any non retry receipts, bubble upwards
                    self.toUpper(protocolTreeNode)

    def processPlaintextNodeAndSend(self, node):
        recipient_id = node["to"].split('@')[0]
        isGroup = "-" in recipient_id

        if node.getChild("media"):
            self.toLower(node) # skip media enc for now, groups and non groups
        elif isGroup:
            self.sendToGroup(node)
        elif self.store.containsSession(recipient_id, 1):
            self.sendToContact(node)
        else:
            self.getKeysFor([node["to"]], lambda: self.sendToContact(node), lambda: self.toLower(node))



    def getPadding(self):
        num = randint(1,127)
        return bytearray([num] * num)

    def groupSendSequence(self):
        """
        check if senderkeyrecord exists
            no: - create,
                - get group jids from info request
                - for each jid without a session, get keys to create the session
                - send message with dist key for all participants
            yes:
                - send skmsg without any dist key

        received retry for a participant
            - request participants keys
            - send message with dist key only + conversation, only for this participat
        :return:
        """

    def enqueueSent(self, node):
        if len(self.sentQueue) >= self.__class__.MAX_SENT_QUEUE:
            logger.warn("Discarding queued node without receipt")
            self.sentQueue.pop(0)
        self.sentQueue.append(node)

    def getEnqueuedMessageNode(self, messageId, keepEnqueued = False):
        for i in range(0, len(self.sentQueue)):
            if self.sentQueue[i]["id"] == messageId:
                if keepEnqueued:
                    return self.sentQueue[i]
                return self.sentQueue.pop(i)


    def sendEncEntities(self, node, encEntities):
        mediaType = None
        messageEntity = EncryptedMessageProtocolEntity(encEntities,
                                           "text" if not mediaType else "media",
                                           _id=node["id"],
                                           to=node["to"],
                                           notify=node["notify"],
                                           timestamp=node["timestamp"],
                                           participant=node["participant"],
                                           offline=node["offline"],
                                           retry=node["retry"]
                                           )
        self.enqueueSent(node)
        self.toLower(messageEntity.toProtocolTreeNode())

    def sendToContact(self, node):
        recipient_id = node["to"].split('@')[0]
        cipher = self.getSessionCipher(recipient_id)
        messageData = self.serializeToProtobuf(node) + self.getPadding()

        ciphertext = cipher.encrypt(messageData)
        mediaType = node.getChild("media")["type"] if node.getChild("media") else None

        return self.sendEncEntities(node, [EncProtocolEntity(EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG, 2, ciphertext.serialize(), mediaType)])

    def sendToGroupWithSessions(self, node, jidsNeedSenderKey = None):
        jidsNeedSenderKey = jidsNeedSenderKey or []
        groupJid = node["to"]
        ownNumber = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(False)
        ownNumber += "@s.whatsapp.net"
        senderKeyName = SenderKeyName(groupJid, AxolotlAddress(ownNumber, 0))
        cipher = self.getGroupCipher(groupJid, ownNumber)
        print(ownNumber)
        encEntities = []
        senderKeyDistributionMessage = self.groupSessionBuilder.create(senderKeyName)
        for jid in jidsNeedSenderKey:
            sessionCipher = self.getSessionCipher(jid.split('@')[0])
            serialized = self.serializeSenderKeyDistributionMessageToProtobuf(node["to"], senderKeyDistributionMessage)
            ciphertext = sessionCipher.encrypt(serialized + self.getPadding())
            encEntities.append(
                EncProtocolEntity(
                        EncProtocolEntity.TYPE_MSG if ciphertext.__class__ == WhisperMessage else EncProtocolEntity.TYPE_PKMSG
                    , 2, ciphertext.serialize(), jid=jid
                )
            )

        messageData = self.serializeToProtobuf(node)
        unciphertext = messageData +  self.getPadding() # bytes([18]) +
       
        # unciphertext = b'\n\x03' + unciphertext[3:]
        #print(type(unciphertext))
        #print(unciphertext)
        #print([s for s in unciphertext])
        #print(len(unciphertext))

        unciphertext = bytes([10]) + bytes([3]) + unciphertext[2:]
        ciphertext = cipher.encrypt(unciphertext.decode())
        
        #print([s for s in ciphertext])
        #print(len(ciphertext))
        mediaType = node.getChild("media")["type"] if node.getChild("media") else None

        encEntities.append(EncProtocolEntity(EncProtocolEntity.TYPE_SKMSG, 2, ciphertext, mediaType))

        self.sendEncEntities(node, encEntities)

    def ensureSessionsAndSendToGroup(self, node, jids):
        jidsNoSession = []
        for jid in jids:
            if not self.store.containsSession(jid.split('@')[0], 1):
                jidsNoSession.append(jid)

        if len(jidsNoSession):
            self.getKeysFor(jidsNoSession, lambda: self.sendToGroupWithSessions(node, jids))
            
        else:
            self.sendToGroupWithSessions(node, jids)

    def sendToGroup(self, node):
        groupJid = node["to"]
        ownNumber = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(False)
        ownNumber += "@s.whatsapp.net"
        ownJid = self.getLayerInterface(YowAuthenticationProtocolLayer).getUsername(True)
        senderKeyName = SenderKeyName(node["to"], AxolotlAddress(ownNumber, 0))
        senderKeyRecord = self.store.loadSenderKey(senderKeyName)


        def sendToGroup(resultNode, requestEntity):
            groupInfo = InfoGroupsResultIqProtocolEntity.fromProtocolTreeNode(resultNode)
            jids = groupInfo.getParticipants().keys()
            return self.ensureSessionsAndSendToGroup(node, [jid for jid in jids if jid != ownJid])

        if senderKeyRecord.isEmpty():
            self.groupSessionBuilder.create(senderKeyName)
            groupInfoIq = InfoGroupsIqProtocolEntity(groupJid)
            self._sendIq(groupInfoIq, sendToGroup)
        else:
            self.sendToGroupWithSessions(node)

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
        return m.SerializeToString()

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

    def serializeSenderKeyDistributionMessageToProtobuf(self, groupId, senderKeyDistributionMessage):
        m = Message()
        sender_key_distribution_message = ProtoSenderKeyDistributionMessage()
        sender_key_distribution_message.groupId = groupId
        sender_key_distribution_message.axolotl_sender_key_distribution_message = senderKeyDistributionMessage.serialize()
        m.sender_key_distribution_message.MergeFrom(sender_key_distribution_message)
        # m.conversation = text
        return m.SerializeToString()
    ###

    def getSessionCipher(self, recipientId):
        if recipientId in self.sessionCiphers:
            sessionCipher = self.sessionCiphers[recipientId]
        else:
            sessionCipher = SessionCipher(self.store, self.store, self.store, self.store, recipientId, 1)
            self.sessionCiphers[recipientId] = sessionCipher

        return sessionCipher

    def getGroupCipher(self, groupId, senderId):
        senderKeyName = SenderKeyName(groupId, AxolotlAddress(senderId, 0))
        if senderKeyName in self.groupCiphers:
            groupCipher = self.groupCiphers[senderKeyName]
        else:
            groupCipher = GroupCipher(self.store, senderKeyName)
            self.groupCiphers[senderKeyName] = groupCipher
        return groupCipher
