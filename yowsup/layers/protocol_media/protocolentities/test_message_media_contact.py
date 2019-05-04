from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import ContactMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class ContactMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(ContactMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ContactMediaMessageProtocolEntity
        m = Message()
        contact_message = Message.ContactMessage()
        contact_message.display_name = "abc"
        contact_message.vcard = b"VCARD_DATA"
        m.contact_message.MergeFrom(contact_message)
        proto_node = self.node.getChild("proto")
        proto_node["mediatype"] = "contact"
        proto_node.setData(m.SerializeToString())
