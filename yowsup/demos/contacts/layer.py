from yowsup.layers.interface                           import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.layers.protocol_contacts.protocolentities  import GetSyncIqProtocolEntity, ResultSyncIqProtocolEntity
from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
import threading
import logging
logger = logging.getLogger(__name__)

class SyncLayer(YowInterfaceLayer):

    PROP_CONTACTS = "org.openwhatsapp.yowsup.prop.syncdemo.contacts"

    def __init__(self):
        super(SyncLayer, self).__init__()

    #call back function when there is a successful connection to whatsapp server
    @ProtocolEntityCallback("success")
    def onSuccess(self, successProtocolEntity):
        contacts= self.getProp(self.__class__.PROP_CONTACTS, [])
        contactEntity = GetSyncIqProtocolEntity(contacts)
        self._sendIq(contactEntity, self.onGetSyncResult, self.onGetSyncError)

    def onGetSyncResult(self, resultSyncIqProtocolEntity, originalIqProtocolEntity):
        print(resultSyncIqProtocolEntity)
        raise KeyboardInterrupt()

    def onGetSyncError(self, errorSyncIqProtocolEntity, originalIqProtocolEntity):
        print(errorSyncIqProtocolEntity)
        raise KeyboardInterrupt()
