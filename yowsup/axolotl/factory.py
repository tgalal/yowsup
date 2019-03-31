from yowsup.axolotl.manager import AxolotlManager
from yowsup.common.tools import StorageTools
from yowsup.axolotl.store.sqlite.liteaxolotlstore import LiteAxolotlStore
import logging

logger = logging.getLogger(__name__)


class AxolotlManagerFactory(object):
    DB = "axolotl.db"

    def get_manager(self, username):
        logger.debug("get_manager(username=%s)" % username)
        dbpath = StorageTools.constructPath(username, self.DB)
        store = LiteAxolotlStore(dbpath)
        return AxolotlManager(store, username)
