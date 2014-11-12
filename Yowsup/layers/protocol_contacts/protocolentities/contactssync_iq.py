from Yowsup.structs import ProtocolTreeNode
from Yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class ContactsSyncIqProtocolEntity(IqProtocolEntity):

    '''
    <iq type="get" id="{{id}}" xmlns="urn:xmpp:whatsapp:sync">
        <sync mode="{{full | ?}}"
            context="{{registration | ?}}"
            sid="{{str((time.time() + 11644477200) * 10000000)}}"
            index="{{0 | ?}}"
            last="{{true | false?}}"
        >
            <user>
                {{num1}}
            </user>
            <user>
                {{num2}}
            </user>

        </sync>
    </iq>
    '''

    def __init__(self, numbers, _id = None, mode = "full", context = "registration", sid = None, index = 0, last = True):
        super(ContactsSyncIqProtocolEntity, self).__init__("urn:xmpp:whatsapp:sync", _id, "get")
        self.setSyncProps(numbers, mode, context, sid, index, last)

    def setSyncProps(self, numbers, mode, context, sid, index, last):
        assert type(numbers) is list, "numbers must be a list"

        self.numbers = numbers
        self.mode = mode
        self.context = context
        self.sid = sid if sid else str((time.time() + 11644477200) * 10000000)
        self.index = int(index)
        self.last = last


    def __str__(self):
        out  = super(ContactsSyncIqProtocolEntity, self).__str__()
        out += "Mode: %s\n" % self.mode
        out += "Context: %s\n" % self.context
        out += "sid: %s\n" % self.sid
        out += "index: %s\n" % self.index
        out += "last: %s\n" % self.last
        out += "numbers: %s\n" % (",".join(self.numbers))
        return out

    def toProtocolTreeNode(self):
        
        syncNodeAttrs = {
            "mode":     self.mode,
            "context":  self.context,
            "sid":      self.sid,
            "index":    str(self.index),
            "last":     "true" if self.last else "false"
        }

        users = [ProtocolTreeNode("user", {}, None, number) for number in self.numbers]
        syncNode = ProtocolTreeNode("sync", syncNodeAttrs, users, None)

        node = super(ContactsSyncIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(syncNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        syncNode         = node.getChild("sync")
        userNodes        = syncNode.getAllChildren()
        numbers          = [userNode.data for userNode in userNodes]
        entity           = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ContactsSyncIqProtocolEntity


        entity.setSyncProps(numbers,
            syncNode.getAttributeValue("mode"),
            syncNode.getAttributeValue("context"),
            syncNode.getAttributeValue("sid"),
            syncNode.getAttributeValue("index"),
            syncNode.getAttributeValue("last")
            )
   

        return entity 
