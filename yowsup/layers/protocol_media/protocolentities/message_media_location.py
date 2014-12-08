from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media import MediaMessageProtocolEntity

class LocationMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
    offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media 
            latitude="52.52393" 
            type="location"
            longitude="13.41747"
            name="Location Name"
            url="http://www.foursquare.com/XXXX"
            encoding="raw"
        >{{THUMBNAIL_RAWDATA}}</media>
    </message>
    '''


    def __init__(self, latitude, longitude, name, url, encoding, _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None):

        super(LocationMediaMessageProtocolEntity, self).__init__("location", _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setLocationMediaProps(latitude,longitude,name,url,encoding)

    def __str__(self):
        out  = super(MediaMessageProtocolEntity, self).__str__()
        out += "Latitude: %s\n" % self.latitude
        out += "Longitude: %s\n" % self.longitude
        out += "Name: %s\n" % self.name
        out += "URL: %s\n" % self.url
        out += "Encoding: %s\n" % self.encoding

        return out

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getLocationName(self):
        return self.name

    def getLocationURL(self):
        return self.url

    def setLocationMediaProps(self, latitude, longitude, locationName, url, encoding):
        self.latitude = latitude
        self.longitude = longitude
        self.name = locationName
        self.url = url
        self.encoding= encoding

    def toProtocolTreeNode(self):
        node = super(LocationMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")
        mediaNode.setAttribute("latitude",  self.latitude)
        mediaNode.setAttribute("longitude",  self.longitude)
        mediaNode.setAttribute("encoding", self.encoding)

        if self.name:
            mediaNode.setAttribute("name", self.name)
        if self.url:
            mediaNode.setAttribute("url", self.url)
            
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = LocationMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setLocationMediaProps(
            mediaNode.getAttributeValue("latitude"),
            mediaNode.getAttributeValue("longitude"),
            mediaNode.getAttributeValue("name"),
            mediaNode.getAttributeValue("url"),
            mediaNode.getAttributeValue("encoding")
            )
        return entity
