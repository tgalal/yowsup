from Yowsup.layers import YowLayer
class YowLoggerLayer(YowLayer):

    def send(self, data):
        print("SEND")
        print(type(data))
        print(data)
        print("----\n")
        self.toLower(data)

    def receive(self, data):
        print("RECEIVE:")
        print(type(data))
        print(data)
        print("----\n")
        self.toUpper(data)


    def __str__(self):
        return "Logger Layer"