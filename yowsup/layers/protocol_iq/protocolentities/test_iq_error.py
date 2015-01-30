from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class ErrorIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        super(ErrorIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ErrorIqProtocolEntity
        self.xml = '''
            <iq id="1417113419-0" from="jid" type="error">
                <error text="not-acceptable" code="406" backoff="3600" />
            </iq>
        '''
