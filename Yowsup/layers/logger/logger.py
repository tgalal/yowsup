from Yowsup.layers import YowLayer
class YowLoggerLayer(YowLayer):

    def send(self, data):
        print("SEND")
        try:
            #print(type(data))
            if type(data) is bytearray:
                print(list(data))
            else:
                print(data)
            print("----\n")
        except UnicodeEncodeError:
            pass
        self.toLower(data)

    def receive(self, data):
        print("RECEIVE:")
        try:
            #print(type(data))
            if type(data) is bytearray:
                print(list(data))
            else:
                print(data)
            print("----\n")
        except UnicodeEncodeError:
            pass
        self.toUpper(data)


    def __str__(self):
        return "Logger Layer"