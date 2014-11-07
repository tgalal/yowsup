from Yowsup.layers import YowLayer
class YowLoggerLayer(YowLayer):

    def send(self, data):
        print("SEND")
        print(data)
        print("----\n")
        self.toLower(data)

    def receive(self, data):
        print("RECEIVE:")
        print(data)
        print("----\n")
        self.toUpper(data)


    def __str__(self):
        return "Logger Layer"