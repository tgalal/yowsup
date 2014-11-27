from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
class ResultIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(ResultIqProtocolEntityTest, self).setUp()
        self.node.setAttribute("type", "result")