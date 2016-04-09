from yowsup.layers.protocol_messages.proto.wa_pb2 import *
from yowsup.layers.axolotl.protocolentities import *

from axolotl.sessionbuilder import SessionBuilder
from axolotl.protocol.whispermessage import WhisperMessage
from axolotl.sessioncipher import SessionCipher
from axolotl.groups.groupcipher import GroupCipher
from axolotl.axolotladdress import AxolotlAddress
from axolotl.groups.senderkeyname import SenderKeyName

import copy
import logging

from .layer_base import AxolotlBaseLayer

logger = logging.getLogger(__name__)

class AxolotlSendLayer(AxolotlBaseLayer):
    def __init__(self):
        super(AxolotlSendLayer, self).__init__()

        self.sessionCiphers = {}
        self.groupCiphers = {}
        self.pendingMessages = {}
        self.skipEncJids = []
        self.v2Jids = []

    def __str__(self):
        return "Axolotl Layer"


    def send(self, node):
        if node.tag == "message" and node["to"] not in self.skipEncJids:
            self.handlePlaintextNode(node)
            return
        self.toLower(node)


    def processPendingMessages(self, jid):
        if jid in self.pendingMessages:
            for messageNode in self.pendingMessages[jid]:
                if jid in self.skipEncJids:
                    self.toLower(messageNode)
                else:
                    self.handlePlaintextNode(messageNode)

            del self.pendingMessages[jid]



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
