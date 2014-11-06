from Yowsup.layers import YowLayer
from Yowsup import ProtocolTreeNode
from textmessage import YowTextMessage
class YowProtocolLayer(YowLayer):
    TYPE_MESSAGE_TEXT = 1;

    def init(self):
        self.currKeyId = 0;
        self.initUpper()
        return True

    def send(self, args):
        if args[0] == YowProtocolLayer.TYPE_MESSAGE:
            node = self.getTextNode(*args[1:])
        else:
            print args[0]
            node = ProtocolTreeNode(args[0], *args[1:])

        self.toLower(node)


    def receive(self, node):
        if ProtocolTreeNode.tagEquals(node, "ib"):
            self.handleIbNode(node)
        elif ProtocolTreeNode.tagEquals(node, "message"):
            self.handleMessageNode(node)
        #else:
        #    self.toUpper(node)

    def handleIbNode(self, node):
        ""

    def handleMessageNode(self, node):
        messageType = node.getAttributeValue("type")
        messageArgs = (
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify")
        )
        if messageType == "text":
            if "@g.us" in node.getAttributeValue("from"):
                #self.toUpper(node)
                return
            message = YowTextMessage(*messageArgs)
            message.setContent(node.getChild("body").getData())
            self.toUpper((YowProtocolLayer.TYPE_MESSAGE_TEXT, message))
        #else:
        #    self.toUpper(node)

    def MessageNode(fn):
        def wrapped(self, *args):
            node = fn(self, *args)
            jid = "broadcast" if type(args[0]) == list else args[0]
            messageNode = self.getMessageNode(jid, node)
            
            return messageNode
            #self.lower.send(messageNode)

            #return messageNode.getAttributeValue("id")
        
        return wrapped

    @MessageNode
    def getTextNode(self,jid, content):
        return ProtocolTreeNode("body",None,None,content);



    def getMessageNode(self, jid, child):
            requestNode = None;
            serverNode = ProtocolTreeNode("server",None);
            xNode = ProtocolTreeNode("x",{"xmlns":"jabber:x:event"},[serverNode]);
            childCount = (0 if requestNode is None else 1) +2;
            messageChildren = []#[None]*childCount;
            if requestNode is not None:
                messageChildren.append(requestNode);


            messageChildren.append(xNode)
            messageChildren.append(ProtocolTreeNode("offline", None))
            
            if type(child) == list:
                messageChildren.extend(child)
            else:
                messageChildren.append(child)
                
            msgId = str(int(time.time()))+"-"+ str(self.currKeyId)
            
            messageNode = ProtocolTreeNode("message",{"to":jid,"type":"text","id":msgId},messageChildren)
            
            self.currKeyId += 1


            return messageNode;

 
