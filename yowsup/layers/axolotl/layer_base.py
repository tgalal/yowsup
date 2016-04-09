from yowsup.layers.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.layers import YowProtocolLayer, YowLayerEvent, EventCallback
from yowsup.common.tools import StorageTools
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer


class AxolotlBaseLayer(YowProtocolLayer):
    _DB = "axolotl.db"
    def __init__(self):
        super(AxolotlBaseLayer, self).__init__()
        self.store = None

    def onNewStoreSet(self, store):
        pass

    def send(self, node):
        self.toLower(node)

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
