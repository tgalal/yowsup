from yowsup.layers.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.layers import YowProtocolLayer
from yowsup.common.tools import StorageTools
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.axolotl.protocolentities import *

from axolotl.sessionbuilder import SessionBuilder

class AxolotlBaseLayer(YowProtocolLayer):
    _DB = "axolotl.db"
    def __init__(self):
        super(AxolotlBaseLayer, self).__init__()
        self.store = None
        self.skipEncJids = []

    def onNewStoreSet(self, store):
        pass

    def send(self, node):
        pass

    def receive(self, node):
        self.processIqRegistry(node)

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
        return self._store

    @store.setter
    def store(self, store):
        self._store = store
        self.onNewStoreSet(self._store)

    def getKeysFor(self, jids, successClbk, errorClbk=None):
        def onSuccess(resultNode, getKeysEntity):
            try:
                entity = ResultGetKeysIqProtocolEntity.fromProtocolTreeNode(resultNode)
            except AttributeError:
                print("Error on resut iq processing!")
                raise
            resultJids = entity.getJids()

            for jid in getKeysEntity.getJids():
                if jid not in resultJids:
                    self.skipEncJids.append(jid)
                    continue

                recipient_id = jid.split('@')[0]
                preKeyBundle = entity.getPreKeyBundleFor(jid)
                sessionBuilder = SessionBuilder(self.store, self.store, self.store, self.store, recipient_id, 1)
                try:
                    sessionBuilder.processPreKeyBundle(preKeyBundle)
                except:
                    print("Identity Failure.")
                    pass
            successClbk()

        def onError(errorNode, getKeysEntity):
            if errorClbk:
                errorClbk()

        entity = GetKeysIqProtocolEntity(jids)
        self._sendIq(entity, onSuccess, onError=onError)
