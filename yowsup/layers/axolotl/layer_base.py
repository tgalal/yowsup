from yowsup.layers.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
from yowsup.layers import YowProtocolLayer
from yowsup.common.tools import StorageTools
from yowsup.layers.auth.layer_authentication import YowAuthenticationProtocolLayer
from yowsup.layers.axolotl.protocolentities import *

from axolotl.sessionbuilder import SessionBuilder
from axolotl.untrustedidentityexception import UntrustedIdentityException
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

import logging
logger = logging.getLogger(__name__)
class AxolotlBaseLayer(YowProtocolLayer):
    _DB = "axolotl.db"
    def __init__(self):
        super(AxolotlBaseLayer, self).__init__()
        self._store = None
        self.skipEncJids = []

    def onNewStoreSet(self, store):
        pass

    def send(self, node):
        pass

    def receive(self, node):
        self.processIqRegistry(node)

    @property
    def store(self):
        try:
            if self._store is None:
                self.store = LiteAxolotlStore(
                    StorageTools.constructPath(
                        self.getProp(
                            YowAuthenticationProtocolLayer.PROP_CREDENTIALS)[0],
                        self.__class__._DB
                    )
                )
            return self._store
        except AttributeError:
            return None

    @store.setter
    def store(self, store):
        self._store = store
        self.onNewStoreSet(self._store)

    def getKeysFor(self, jids, resultClbk, errorClbk = None):
        def onSuccess(resultNode, getKeysEntity):
            entity = ResultGetKeysIqProtocolEntity.fromProtocolTreeNode(resultNode)
            resultJids = entity.getJids()
            successJids = []
            errorJids = {} #jid -> exception

            for jid in getKeysEntity.getJids():
                if jid not in resultJids:
                    self.skipEncJids.append(jid)
                    continue

                recipient_id = jid.split('@')[0]
                preKeyBundle = entity.getPreKeyBundleFor(jid)
                sessionBuilder = SessionBuilder(self.store, self.store, self.store, self.store, recipient_id, 1)
                try:
                    sessionBuilder.processPreKeyBundle(preKeyBundle)
                    successJids.append(jid)
                except UntrustedIdentityException as e:
                    if self.getProp(PROP_IDENTITY_AUTOTRUST, False):
                        logger.warning("Autotrusting identity for %s" % e.getName())
                        self.store.saveIdentity(e.getName(), e.getIdentityKey())
                        successJids.append(jid)
                    else:
                        errorJids[jid] = e
                        logger.error(e)
                        logger.warning("Ignoring message with untrusted identity")

                resultClbk(successJids, errorJids)

        def onError(errorNode, getKeysEntity):
            if errorClbk:
                errorClbk(errorNode, getKeysEntity)

        entity = GetKeysIqProtocolEntity(jids)
        self._sendIq(entity, onSuccess, onError=onError)
