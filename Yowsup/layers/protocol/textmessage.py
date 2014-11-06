from message import YowMessage

class YowTextMessage(YowMessage):
    def __init__(self, *args):
        YowMessage.__init__(self, *args)
        self._content = None

    def setContent(self, content):
        self._content = content

    def getContent(self):
        return self._content

    def __str__(self):
        return self.getContent()