import importlib
import logging
logger = logging.getLogger(__name__)
from contextlib import contextmanager

class OptionalModule(object):
    def __init__(self, modulename, failMessage = None, require = False):
        self.modulename = modulename
        self.require = require
        self.failMessage = failMessage

    def __enter__(self):
        return self.importFn

    def importFn(self, what = None):
        imp = self.modulename if not what else ("%s.%s" % (self.modulename, what))
        return importlib.import_module(imp)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if isinstance(exc_val, ImportError):
            failMessage = self.failMessage if self.failMessage is not None else ("%s import failed" % self.modulename)
            if failMessage:
                logger.error(failMessage)
            if self.require:
                raise
            return True

class PILOptionalModule(OptionalModule):
    def __init__(self, failMessage = None, require = False):
        super(PILOptionalModule, self).__init__("PIL",
                failMessage= failMessage,
                require = require)

class FFVideoOptionalModule(OptionalModule):
    def __init__(self, failMessage = None, require = False):
        super(FFVideoOptionalModule, self).__init__("ffvideo",
                failMessage=failMessage,
                require=require)

class AxolotlOptionalModule(OptionalModule):
    def __init__(self, failMessage = None, require = False):
        super(AxolotlOptionalModule, self).__init__("axolotl",
                failMessage=failMessage,
                require=require)

if __name__ == "__main__":
    with PILOptionalModule() as imp:
        imp()
        print("OK")
    print("DONE")
