from yowsup.layers import YowLayer
import logging
logger = logging.getLogger(__name__)
class YowLoggerLayer(YowLayer):

    def send(self, data):
        ldata = list(data) if type(data) is bytearray else data
        logger.debug("tx:\n%s" % ldata)
        self.toLower(data)

    def receive(self, data):
        ldata = list(data) if type(data) is bytearray else data
        logger.debug("rx:\n%s" % ldata)
        self.toUpper(data)

    def __str__(self):
        return "Logger Layer"