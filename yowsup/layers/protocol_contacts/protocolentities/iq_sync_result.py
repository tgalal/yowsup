from yowsup.structs import ProtocolTreeNode
from .iq_sync import SyncIqProtocolEntity

class ResultSyncIqProtocolEntity(SyncIqProtocolEntity):
    '''
    <iq type="result" from="491632092557@s.whatsapp.net" id="1417046561-4">
    <sync index="0" wait="166952" last="true" version="1417046548593182" sid="1.30615237617e+17">
        <in>
            <user jid="{{jid}}>{{number}}</user>
        </in>
        <out>
            <user jid="{{jid}}">
            {{number}}
        </user>
        </out>
        <invalid>
            <user>
                abcdefgh
            </user>
        </invalid>

    </sync>
    </iq>
    '''

    def __init__(self,_id, sid, index, last, version, inNumbers, outNumbers, invalidNumbers, wait = None):
        super(ResultSyncIqProtocolEntity, self).__init__("result", _id, sid, index, last)
        self.setResultSyncProps(wait, version, inNumbers, outNumbers, invalidNumbers)

    def setResultSyncProps(self, version, inNumbers, outNumbers, invalidNumbers, wait = None):
        assert type(inNumbers) is dict, "in numbers must be a dict {number -> jid}"
        assert type(outNumbers) is dict, "out numbers must be a dict {number -> jid}"
        assert type(invalidNumbers) is list, "invalid numbers must be a list"

        self.inNumbers = inNumbers
        self.outNumbers = outNumbers
        self.invalidNumbers = invalidNumbers
        self.wait = int(wait) if wait is not None else None
        self.version = version


    def __str__(self):
        out  = super(SyncIqProtocolEntity, self).__str__()
        if self.wait is not None:
            out += "Wait: %s\n" % self.wait
        out += "Version: %s\n" % self.version
        out += "In Numbers: %s\n" % (",".join(self.inNumbers))
        out += "Out Numbers: %s\n" % (",".join(self.outNumbers))
        out += "Invalid Numbers: %s\n" % (",".join(self.invalidNumbers))

        return out

    def toProtocolTreeNode(self):
        
        outUsers = [ProtocolTreeNode("user", {"jid": jid}, None, number) for number, jid in self.outNumbers.items()]
        inUsers = [ProtocolTreeNode("user", {"jid": jid}, None, number) for number, jid in self.inNumbers.items()]
        invalidUsers = [ProtocolTreeNode("user", {}, None, number) for number in self.invalidNumbers]

        node = super(ResultSyncIqProtocolEntity, self).toProtocolTreeNode()
        syncNode = node.getChild("sync")
        syncNode.setAttribute("version", self.version)

        if self.wait is not None:
            syncNode.setAttribute("wait", str(self.wait))

        if len(outUsers):
            syncNode.addChild(ProtocolTreeNode("out", children = outUsers))

        if len(inUsers):
            syncNode.addChild(ProtocolTreeNode("in", children = inUsers))

        if len(invalidUsers):
            syncNode.addChildren([ProtocolTreeNode("invalid", children = invalidUsers)])

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        syncNode         = node.getChild("sync")
        outNode          = syncNode.getChild("out")
        inNode           = syncNode.getChild("in")
        invalidNode      = syncNode.getChild("invalid")
        outUsers         = outNode.getAllChildren() if outNode else []
        inUsers          = inNode.getAllChildren()  if inNode else []
        invalidUsers     = [inode.data for inode in invalidNode.getAllChildren()] if invalidNode else []

        outUsersDict = {}
        for u in outUsers:
            outUsersDict[u.data] = u.getAttributeValue("jid")

        inUsersDict = {}
        for u in inUsers:
            inUsersDict[u.data] = u.getAttributeValue("jid")

        entity           = SyncIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ResultSyncIqProtocolEntity

        entity.setResultSyncProps(syncNode.getAttributeValue("version"),
            inUsersDict,
            outUsersDict,
            invalidUsers,
            syncNode.getAttributeValue("wait")
            )
   
        return entity
