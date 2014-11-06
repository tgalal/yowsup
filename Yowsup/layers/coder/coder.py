from Yowsup.layers import YowLayer
from writer import Writer
from reader import Reader
class YowCoderLayer(YowLayer):
    def __init__(self):
        YowLayer.__init__(self)
        self.writer = Writer(self)
        self.reader = Reader(self)
        self.readBuf = []
        self.readStreamStarted = False
    def init(self):
        self.writer.streamStart(
            self.__class__.getProp("domain"),
            self.__class__.getProp("resource")
        )
        self.initUpper()
        return True

    def send(self, data):
        self.writer.write(data)

    def receive(self, data):
        self.readBuf = self.readBuf + data
        if not self.readStreamStarted:
            self.readStreamStarted = True
            self.reader.streamStart()
            #self.toUpper(self.reader.nextTree())
        else:
            self.toUpper(self.reader.nextTree())

    def write(self, i):
        if(type(i) in(list, tuple)):
            self.toLower(i)
        else:
            self.toLower((i,))


    def readAll(self):
        result = self.readBuf
        self.readBuf = []
        return result

    def read(self, _ = None):
        return self.readBuf.pop(0)