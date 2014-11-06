class ReceiveParser:
    def parse(self, node):
        if ProtocolTreeNode.tagEquals(node,"message"):
            self.parseMessage(node)

    def parseMessage(node):
        pass