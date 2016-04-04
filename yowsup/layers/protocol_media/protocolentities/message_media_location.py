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
            preview = None, offline = None, retry = None, description = None):

        super(LocationMediaMessageProtocolEntity, self).__init__("location", _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setLocationMediaProps(latitude,longitude,name,url,encoding, description)

    def __str__(self):
        out  = super(MediaMessageProtocolEntity, self).__str__()
        out += "Latitude: %s\n" % self.latitude
        out += "Longitude: %s\n" % self.longitude
        out += "Name: %s\n" % self.name
        out += "URL: %s\n" % self.url
        out += "Encoding: %s\n" % self.encoding
        out += "Description: %s\n" % self.description

        return out

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getLocationName(self):
        return self.name

    def getLocationURL(self):
        return self.url

    def getDescription(self):
        return self.description

    def setLocationMediaProps(self, latitude, longitude, locationName, url, encoding, description):
        self.latitude = str(latitude)
        self.longitude = str(longitude)
        self.name = locationName
        self.url = url
        self.encoding = encoding
        self.description = description

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
        if self.description:
            mediaNode.setAttribute("description", self.description)

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
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("description")
            )
        return entity