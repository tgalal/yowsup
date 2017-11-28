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


    def __init__(self, latitude, longitude, name=None, url=None, encoding=None, _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None, address = None):

        super(LocationMediaMessageProtocolEntity, self).__init__("location", _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setLocationMediaProps(latitude,longitude,name,address, url)

    def __str__(self):
        out  = super(MediaMessageProtocolEntity, self).__str__()
        out += "Latitude: %s\n" % self.latitude
        out += "Longitude: %s\n" % self.longitude
        out += "Name: %s\n" % self.name
        out += "Address: %s\n" % self.address
        out += "URL: %s\n" % self.url

        return out

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getLocationName(self):
        return self.name

    def getLocationURL(self):
        return self.url

    def getAddress(self):
        return self.address


    def setLocationMediaProps(self, latitude, longitude, locationName=None, address=None, url=None):
        self.latitude = str(latitude)
        self.longitude = str(longitude)
        self.name = str(locationName)
        self.address = str(address)
        self.url = str(url)

    def toProtocolTreeNode(self):
        node = super(LocationMediaMessageProtocolEntity, self).toProtocolTreeNode()
        print("TO PROTOCOL TREE NODE")
        print(node)

        mediaNode = node.getChild("enc")

        mediaNode.setAttribute("latitude",  self.latitude)
        mediaNode.setAttribute("longitude",  self.longitude)

        if self.name:
            mediaNode.setAttribute("name", self.name)
        if self.address:
            mediaNode.setAttribute("address", self.address)
        if self.url:
            mediaNode.setAttribute("url", self.url)

        print(mediaNode)

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
            mediaNode.getAttributeValue("address")
        )
        return entity
