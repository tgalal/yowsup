from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media import MediaMessageProtocolEntity

class UrlMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
    offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media 
            type="url"
            text="Hi, look https://www.google.com/search?q=yowsup"
            match="https://www.google.com/search?q=yowsup"
            url="https://www.google.com"
            description="yowsup - Search with google - Mozilla Firefox"
            title="yowsup - Search with google"
        >{{THUMBNAIL_RAWDATA}}</media>
    </message>
    '''


    def __init__(self, text, match, url, description, title, _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None):

        super(UrlMediaMessageProtocolEntity, self).__init__("url", _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setUrlMediaProps(text, match, url, description, title)

    def __str__(self):
        out  = super(MediaMessageProtocolEntity, self).__str__()
        out += "Text: %s\n" % self.text
        #out += "Match: %s\n" % self.match
        #out += "Url: %s\n" % self.url
        #out += "Description: %s\n" % self.description
        #out += "Title: %s\n" % self.title
        return out

    def getText(self):
        return self.text

    def getMatch(self):
        return self.match

    def getTitle(self):
        return self.title

    def getURL(self):
        return self.url

    def getDescription(self):
        return self.description

    def setUrlMediaProps(self, text, match, url, description, title):
        self.text = text
        self.match = match
        self.url = url
        self.description = description
        self.title = title

    def toProtocolTreeNode(self):
        node = super(UrlMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")
        mediaNode.setAttribute("text",  self.text)
        mediaNode.setAttribute("match",  self.match)
        mediaNode.setAttribute("title", self.name)
        mediaNode.setAttribute("url", self.url)
        mediaNode.setAttribute("description", self.description)
            
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = UrlMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setUrlMediaProps(
            mediaNode.getAttributeValue("text"),
            mediaNode.getAttributeValue("match"),
            mediaNode.getAttributeValue("url"),
            mediaNode.getAttributeValue("description"),
            mediaNode.getAttributeValue("title"),
            )
        return entity
