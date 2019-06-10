from .cli import Cli, clicmd
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers import YowLayerEvent, EventCallback
from yowsup.layers.network import YowNetworkLayer
import sys
from yowsup.common import YowConstants
import datetime
import time
import os
import logging
import threading
import base64
from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.protocol_presence.protocolentities    import *
from yowsup.layers.protocol_messages.protocolentities    import *
from yowsup.layers.protocol_ib.protocolentities          import *
from yowsup.layers.protocol_iq.protocolentities          import *
from yowsup.layers.protocol_contacts.protocolentities    import *
from yowsup.layers.protocol_chatstate.protocolentities   import *
from yowsup.layers.protocol_privacy.protocolentities     import *
from yowsup.layers.protocol_media.protocolentities       import *
from yowsup.layers.protocol_media.mediauploader import MediaUploader
from yowsup.layers.protocol_profiles.protocolentities    import *
from yowsup.common.tools import Jid
from yowsup.common.optionalmodules import PILOptionalModule
from yowsup.layers.axolotl.protocolentities.iq_key_get import GetKeysIqProtocolEntity

logger = logging.getLogger(__name__)
class YowsupCliLayer(Cli, YowInterfaceLayer):
    PROP_RECEIPT_AUTO       = "org.openwhatsapp.yowsup.prop.cli.autoreceipt"
    PROP_RECEIPT_KEEPALIVE  = "org.openwhatsapp.yowsup.prop.cli.keepalive"
    PROP_CONTACT_JID        = "org.openwhatsapp.yowsup.prop.cli.contact.jid"
    EVENT_LOGIN             = "org.openwhatsapp.yowsup.event.cli.login"
    EVENT_START             = "org.openwhatsapp.yowsup.event.cli.start"
    EVENT_SENDANDEXIT       = "org.openwhatsapp.yowsup.event.cli.sendandexit"

    MESSAGE_FORMAT          = "[%s(%s)]:[%s]\t %s"

    FAIL_OPT_PILLOW         = "No PIL library installed, try install pillow"
    FAIL_OPT_AXOLOTL        = "axolotl is not installed, try install python-axolotl"

    DISCONNECT_ACTION_PROMPT = 0
    DISCONNECT_ACTION_EXIT   = 1

    ACCOUNT_DEL_WARNINGS = 4

    def __init__(self):
        super(YowsupCliLayer, self).__init__()
        YowInterfaceLayer.__init__(self)
        self.accountDelWarnings = 0
        self.connected = False
        self.username = None
        self.sendReceipts = True
        self.sendRead = True
        self.disconnectAction = self.__class__.DISCONNECT_ACTION_PROMPT

        #add aliases to make it user to use commands. for example you can then do:
        # /message send foobar "HI"
        # and then it will get automaticlaly mapped to foobar's jid
        self.jidAliases = {
            # "NAME": "PHONE@s.whatsapp.net"
        }

    def aliasToJid(self, calias):
        for alias, ajid in self.jidAliases.items():
            if calias.lower() == alias.lower():
                return Jid.normalize(ajid)

        return Jid.normalize(calias)

    def jidToAlias(self, jid):
        for alias, ajid in self.jidAliases.items():
            if ajid == jid:
                return alias
        return jid

    @EventCallback(EVENT_START)
    def onStart(self, layerEvent):
        self.startInput()
        return True

    @EventCallback(YowNetworkLayer.EVENT_STATE_DISCONNECTED)
    def onStateDisconnected(self,layerEvent):
        self.output("Disconnected: %s" % layerEvent.getArg("reason"))
        if self.disconnectAction == self.__class__.DISCONNECT_ACTION_PROMPT:
           self.connected = False
           self.notifyInputThread()
        else:
           os._exit(os.EX_OK)

    def assertConnected(self):
        if self.connected:
            return True
        else:
            self.output("Not connected", tag = "Error", prompt = False)
            return False

    ########## PRESENCE ###############
    @clicmd("Set presence name")
    def presence_name(self, name):
        if self.assertConnected():
            entity = PresenceProtocolEntity(name = name)
            self.toLower(entity)

    @clicmd("Set presence as available")
    def presence_available(self):
        if self.assertConnected():
            entity = AvailablePresenceProtocolEntity()
            self.toLower(entity)

    @clicmd("Set presence as unavailable")
    def presence_unavailable(self):
        if self.assertConnected():
            entity = UnavailablePresenceProtocolEntity()
            self.toLower(entity)

    @clicmd("Unsubscribe from contact's presence updates")
    def presence_unsubscribe(self, contact):
        if self.assertConnected():
            entity = UnsubscribePresenceProtocolEntity(self.aliasToJid(contact))
            self.toLower(entity)

    @clicmd("Subscribe to contact's presence updates")
    def presence_subscribe(self, contact):
        if self.assertConnected():
            entity = SubscribePresenceProtocolEntity(self.aliasToJid(contact))
            self.toLower(entity)

    ########### END PRESENCE #############

    ########### ib #######################
    @clicmd("Send clean dirty")
    def ib_clean(self, dirtyType):
        if self.assertConnected():
            entity = CleanIqProtocolEntity("groups", YowConstants.DOMAIN)
            self.toLower(entity)

    @clicmd("Ping server")
    def ping(self):
        if self.assertConnected():
            entity = PingIqProtocolEntity(to = YowConstants.DOMAIN)
            self.toLower(entity)

    ######################################

    ####### contacts/ profiles ####################
    @clicmd("Set status text")
    def profile_setStatus(self, text):
        if self.assertConnected():

            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Status updated successfully")

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error updating status")

            entity = SetStatusIqProtocolEntity(text)
            self._sendIq(entity, onSuccess, onError)

    @clicmd("Get profile picture for contact")
    def contact_picture(self, jid):
        if self.assertConnected():
            entity = GetPictureIqProtocolEntity(self.aliasToJid(jid), preview=False)
            self._sendIq(entity, self.onGetContactPictureResult)

    @clicmd("Get profile picture preview for contact")
    def contact_picturePreview(self, jid):
        if self.assertConnected():
            entity = GetPictureIqProtocolEntity(self.aliasToJid(jid), preview=True)
            self._sendIq(entity, self.onGetContactPictureResult)

    @clicmd("Get lastseen for contact")
    def contact_lastseen(self, jid):
        if self.assertConnected():
            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("%s lastseen %s seconds ago" % (resultIqEntity.getFrom(), resultIqEntity.getSeconds()))

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error getting lastseen information for %s" % originalIqEntity.getTo())

            entity = LastseenIqProtocolEntity(self.aliasToJid(jid))
            self._sendIq(entity, onSuccess, onError)

    @clicmd("Set profile picture")
    def profile_setPicture(self, path):
        if self.assertConnected():
            with PILOptionalModule(failMessage = "No PIL library installed, try install pillow") as imp:
                Image = imp("Image")
                def onSuccess(resultIqEntity, originalIqEntity):
                    self.output("Profile picture updated successfully")

                def onError(errorIqEntity, originalIqEntity):
                    logger.error("Error updating profile picture")

                #example by @aesedepece in https://github.com/tgalal/yowsup/pull/781
                #modified to support python3
                src = Image.open(path)
                pictureData = src.resize((640, 640)).tobytes("jpeg", "RGB")
                picturePreview = src.resize((96, 96)).tobytes("jpeg", "RGB")
                iq = SetPictureIqProtocolEntity(self.getOwnJid(), picturePreview, pictureData)
                self._sendIq(iq, onSuccess, onError)

    @clicmd("Get profile privacy")
    def profile_getPrivacy(self):
        if self.assertConnected():
            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Profile privacy is: %s" %(resultIqEntity))

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error getting profile privacy")

            iq = GetPrivacyIqProtocolEntity()
            self._sendIq(iq, onSuccess, onError)

    @clicmd("Profile privacy. value=all|contacts|none names=profile|status|last. Names are comma separated, defaults to all.")
    def profile_setPrivacy(self, value="all", names=None):
        if self.assertConnected():
            def onSuccess(resultIqEntity, originalIqEntity):
                self.output("Profile privacy set to: %s" %(resultIqEntity))

            def onError(errorIqEntity, originalIqEntity):
                logger.error("Error setting profile privacy")
            try:
                names = [name for name in names.split(',')] if names else None
                iq = SetPrivacyIqProtocolEntity(value, names)
                self._sendIq(iq, onSuccess, onError)
            except Exception as inst:
                self.output(inst.message)
                return self.print_usage()


    ########### groups

    @clicmd("List all groups you belong to", 5)
    def groups_list(self):
        if self.assertConnected():
            entity = ListGroupsIqProtocolEntity()
            self.toLower(entity)

    @clicmd("Leave a group you belong to", 4)
    def group_leave(self, group_jid):
        if self.assertConnected():
            entity = LeaveGroupsIqProtocolEntity([self.aliasToJid(group_jid)])
            self.toLower(entity)

    @clicmd("Create a new group with the specified subject and participants. Jids are a comma separated list but optional.", 3)
    def groups_create(self, subject, jids = None):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')] if jids else []
            entity = CreateGroupsIqProtocolEntity(subject, participants=jids)
            self.toLower(entity)

    @clicmd("Invite to group. Jids are a comma separated list")
    def group_invite(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = AddParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Promote admin of a group. Jids are a comma separated list")
    def group_promote(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = PromoteParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Remove admin of a group. Jids are a comma separated list")
    def group_demote(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = DemoteParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Kick from group. Jids are a comma separated list")
    def group_kick(self, group_jid, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = RemoveParticipantsIqProtocolEntity(self.aliasToJid(group_jid), jids)
            self.toLower(entity)

    @clicmd("Change group subject")
    def group_setSubject(self, group_jid, subject):
        if self.assertConnected():
            entity = SubjectGroupsIqProtocolEntity(self.aliasToJid(group_jid), subject)
            self.toLower(entity)

    @clicmd("Set group picture")
    def group_picture(self, group_jid, path):
        if self.assertConnected():
            with PILOptionalModule(failMessage = self.__class__.FAIL_OPT_PILLOW) as imp:
                Image = imp("Image")

                def onSuccess(resultIqEntity, originalIqEntity):
                    self.output("Group picture updated successfully")

                def onError(errorIqEntity, originalIqEntity):
                    logger.error("Error updating Group picture")

                #example by @aesedepece in https://github.com/tgalal/yowsup/pull/781
                #modified to support python3
                src = Image.open(path)
                pictureData = src.resize((640, 640)).tobytes("jpeg", "RGB")
                picturePreview = src.resize((96, 96)).tobytes("jpeg", "RGB")
                iq = SetPictureIqProtocolEntity(self.aliasToJid(group_jid), picturePreview, pictureData)
                self._sendIq(iq, onSuccess, onError)


    @clicmd("Get group info")
    def group_info(self, group_jid):
        if self.assertConnected():
            entity = InfoGroupsIqProtocolEntity(self.aliasToJid(group_jid))
            self.toLower(entity)

    @clicmd("Get shared keys")
    def keys_get(self, jids):
        if self.assertConnected():
            jids = [self.aliasToJid(jid) for jid in jids.split(',')]
            entity = GetKeysIqProtocolEntity(jids)
            self.toLower(entity)

    @clicmd("Send init seq")
    def seq(self):
        priv = PrivacyListIqProtocolEntity()
        self.toLower(priv)
        push = PushIqProtocolEntity()
        self.toLower(push)
        props = PropsIqProtocolEntity()
        self.toLower(props)
        crypto = CryptoIqProtocolEntity()
        self.toLower(crypto)

    @clicmd("Delete your account")
    def account_delete(self):
        if self.assertConnected():
            if self.accountDelWarnings < self.__class__.ACCOUNT_DEL_WARNINGS:
                self.accountDelWarnings += 1
                remaining = self.__class__.ACCOUNT_DEL_WARNINGS - self.accountDelWarnings
                self.output("Repeat delete command another %s times to send the delete request" % remaining, tag="Account delete Warning !!", prompt = False)
            else:
                entity = UnregisterIqProtocolEntity()
                self.toLower(entity)

    @clicmd("Send message to a friend")
    def message_send(self, number, content):
        if self.assertConnected():
            outgoingMessage = TextMessageProtocolEntity(content, to=self.aliasToJid(number))
            self.toLower(outgoingMessage)

    @clicmd("Broadcast message. numbers should comma separated phone numbers")
    def message_broadcast(self, numbers, content):
        if self.assertConnected():
            jids = [self.aliasToJid(number) for number in numbers.split(',')]
            outgoingMessage = BroadcastTextMessage(jids, content)
            self.toLower(outgoingMessage)

    #@clicmd("Send read receipt")
    def message_read(self, message_id):
        pass

    #@clicmd("Send delivered receipt")
    def message_delivered(self, message_id):
        pass

    @clicmd("Send a video with optional caption")
    def video_send(self, number, path, caption = None):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO)

    @clicmd("Send an image with optional caption")
    def image_send(self, number, path, caption = None):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE)

    @clicmd("Send audio file")
    def audio_send(self, number, path):
        self.media_send(number, path, RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO)

    def media_send(self, number, path, mediaType, caption = None):
        if self.assertConnected():
            jid = self.aliasToJid(number)
            entity = RequestUploadIqProtocolEntity(mediaType, filePath=path)
            successFn = lambda successEntity, originalEntity: self.onRequestUploadResult(jid, mediaType, path, successEntity, originalEntity, caption)
            errorFn = lambda errorEntity, originalEntity: self.onRequestUploadError(jid, path, errorEntity, originalEntity)
            self._sendIq(entity, successFn, errorFn)

    @clicmd("Send typing state")
    def state_typing(self, jid):
        if self.assertConnected():
            entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_TYPING, self.aliasToJid(jid))
            self.toLower(entity)

    @clicmd("Request contacts statuses")
    def statuses_get(self, contacts):

        def on_success(entity, original_iq_entity):
            # type: (ResultStatusesIqProtocolEntity, GetStatusesIqProtocolEntity) -> None
            status_outs = []
            for jid, status_info in entity.statuses.items():
                status_outs.append("[user=%s status=%s last_updated=%s]" % (jid, status_info[0], status_info[1]))
            self.output("\n".join(status_outs), tag="statuses_get result")

        def on_error(entity, original_iq):
            # type: (ResultStatusesIqProtocolEntity, GetStatusesIqProtocolEntity) -> None
            logger.error("Failed to get statuses")

        if self.assertConnected():
            entity = GetStatusesIqProtocolEntity([self.aliasToJid(c) for c in contacts.split(',')])
            self._sendIq(entity, on_success, on_error)

    @clicmd("Send paused state")
    def state_paused(self, jid):
        if self.assertConnected():
            entity = OutgoingChatstateProtocolEntity(ChatstateProtocolEntity.STATE_PAUSED, self.aliasToJid(jid))
            self.toLower(entity)

    @clicmd("Sync contacts, contacts should be comma separated phone numbers, with no spaces")
    def contacts_sync(self, contacts):
        if self.assertConnected():
            entity = GetSyncIqProtocolEntity(contacts.split(','))
            self.toLower(entity)

    @clicmd("Disconnect")
    def disconnect(self):
        if self.assertConnected():

            self.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_DISCONNECT))

    @clicmd("Quick login")
    def L(self):
        if self.connected:
            return self.output("Already connected, disconnect first")
        threading.Thread(target=lambda: self.getLayerInterface(YowNetworkLayer).connect()).start()
        return True

    ######## receive #########
    
    @ProtocolEntityCallback("presence")
    def onPresenceChange(self, entity):
        status="offline"
        if entity.getType() is None:
            status="online"     
        ##raw fix for iphone lastseen deny output
        lastseen = entity.getLast()
        if status is "offline" and lastseen is "deny":
            lastseen = time.time()
        ##
        self.output("%s %s %s lastseen at: %s" % (entity.getFrom(), entity.getTag(), status, lastseen))
        
    @ProtocolEntityCallback("chatstate")
    def onChatstate(self, entity):
        print(entity)

    @ProtocolEntityCallback("iq")
    def onIq(self, entity):
        if not isinstance(entity, ResultStatusesIqProtocolEntity):  # already printed somewhere else
            print(entity)

    @ProtocolEntityCallback("receipt")
    def onReceipt(self, entity):
        self.toLower(entity.ack())

    @ProtocolEntityCallback("ack")
    def onAck(self, entity):
        #formattedDate = datetime.datetime.fromtimestamp(self.sentCache[entity.getId()][0]).strftime('%d-%m-%Y %H:%M')
        #print("%s [%s]:%s"%(self.username, formattedDate, self.sentCache[entity.getId()][1]))
        if entity.getClass() == "message":
            self.output(entity.getId(), tag = "Sent")
            #self.notifyInputThread()

    @ProtocolEntityCallback("success")
    def onSuccess(self, entity):
        self.connected = True
        self.output("Logged in!", "Auth", prompt = False)
        self.notifyInputThread()

    @ProtocolEntityCallback("failure")
    def onFailure(self, entity):
        self.connected = False
        self.output("Login Failed, reason: %s" % entity.getReason(), prompt = False)

    @ProtocolEntityCallback("notification")
    def onNotification(self, notification):
        notificationData = notification.__str__()
        if notificationData:
            self.output(notificationData, tag = "Notification")
        else:
            self.output("From :%s, Type: %s" % (self.jidToAlias(notification.getFrom()), notification.getType()), tag = "Notification")

    @ProtocolEntityCallback("message")
    def onMessage(self, message):
        messageOut = ""
        if message.getType() == "text":
            #self.output(message.getBody(), tag = "%s [%s]"%(message.getFrom(), formattedDate))
            messageOut = self.getTextMessageBody(message)
        elif message.getType() == "media":
            messageOut = self.getMediaMessageBody(message)
        else:
            messageOut = "Unknown message type %s " % message.getType()
            print(messageOut.toProtocolTreeNode())

        formattedDate = datetime.datetime.fromtimestamp(message.getTimestamp()).strftime('%d-%m-%Y %H:%M')
        sender = message.getFrom() if not message.isGroupMessage() else "%s/%s" % (message.getParticipant(False), message.getFrom())

        output = self.__class__.MESSAGE_FORMAT % (sender, formattedDate, message.getId(), messageOut)

        self.output(output, tag = None, prompt = not self.sendReceipts)
        if self.sendReceipts:
            self.toLower(message.ack(self.sendRead))
            self.output("Sent delivered receipt"+" and Read" if self.sendRead else "", tag = "Message %s" % message.getId())

    def getTextMessageBody(self, message):
        if isinstance(message, TextMessageProtocolEntity):
            return message.conversation
        elif isinstance(message, ExtendedTextMessageProtocolEntity):
            return str(message.message_attributes.extended_text)
        else:
            raise NotImplementedError()

    def getMediaMessageBody(self, message):
        # type: (DownloadableMediaMessageProtocolEntity) -> str
        return str(message.message_attributes)

    def getDownloadableMediaMessageBody(self, message):
        return "[media_type={media_type}, length={media_size}, url={media_url}, key={media_key}]".format(
            media_type=message.media_type,
            media_size=message.file_length,
            media_url=message.url,
            media_key=base64.b64encode(message.media_key)
        )

    def doSendMedia(self, mediaType, filePath, url, to, ip = None, caption = None):
        if mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_IMAGE:
        	entity = ImageDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_AUDIO:
        	entity = AudioDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to)
        elif mediaType == RequestUploadIqProtocolEntity.MEDIA_TYPE_VIDEO:
        	entity = VideoDownloadableMediaMessageProtocolEntity.fromFilePath(filePath, url, ip, to, caption = caption)
        self.toLower(entity)

    def __str__(self):
        return "CLI Interface Layer"

    ########### callbacks ############

    def onRequestUploadResult(self, jid, mediaType, filePath, resultRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity, caption = None):

        if resultRequestUploadIqProtocolEntity.isDuplicate():
            self.doSendMedia(mediaType, filePath, resultRequestUploadIqProtocolEntity.getUrl(), jid,
                             resultRequestUploadIqProtocolEntity.getIp(), caption)
        else:
            successFn = lambda filePath, jid, url: self.doSendMedia(mediaType, filePath, url, jid, resultRequestUploadIqProtocolEntity.getIp(), caption)
            mediaUploader = MediaUploader(jid, self.getOwnJid(), filePath,
                                      resultRequestUploadIqProtocolEntity.getUrl(),
                                      resultRequestUploadIqProtocolEntity.getResumeOffset(),
                                      successFn, self.onUploadError, self.onUploadProgress, asynchronous=False)
            mediaUploader.start()

    def onRequestUploadError(self, jid, path, errorRequestUploadIqProtocolEntity, requestUploadIqProtocolEntity):
        logger.error("Request upload for file %s for %s failed" % (path, jid))

    def onUploadError(self, filePath, jid, url):
        logger.error("Upload file %s to %s for %s failed!" % (filePath, url, jid))

    def onUploadProgress(self, filePath, jid, url, progress):
        sys.stdout.write("%s => %s, %d%% \r" % (os.path.basename(filePath), jid, progress))
        sys.stdout.flush()

    def onGetContactPictureResult(self, resultGetPictureIqProtocolEntiy, getPictureIqProtocolEntity):
        # do here whatever you want
        # write to a file
        # or open
        # or do nothing
        # write to file example:
        #resultGetPictureIqProtocolEntiy.writeToFile("/tmp/yowpics/%s_%s.jpg" % (getPictureIqProtocolEntity.getTo(), "preview" if resultGetPictureIqProtocolEntiy.isPreview() else "full"))
        pass

    @clicmd("Print this message")
    def help(self):
        self.print_usage()
