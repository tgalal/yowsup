from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media import MediaMessageProtocolEntity

class VCardMediaMessageProtocolEntity(MediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}"
    offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media type="vcard">
            <vcard name="Hany Yasser">
                BEGIN:VCARD
                VERSION:3.0
                N:Yasser;Hany;;;
                FN:Hany Yasser
                PHOTO;BASE64:/9j/4AAQSkZJRgABAQEASABIAAD/4QBYRXhpZgAATU0AKgAAAAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAQKADAAQAAAABAAAAQAAAAAD/7QA4UGhvdG9zaG9wIDMuMAA4QklNBAQAAAAAAAA4QklNBCUAAAAAABDUHYzZjwCyBOmACZjs+EJ+/8AAEQgAQABAAwEiAAIRAQMRAf/EAB8AAAEFAQEBAQEBAAAAAAAAAAABAgMEBQYHCAkKC//EALUQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYXGBkaJSYnKCkqNDU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6g4SFhoeIiYqSk5SVlpeYmZqio6Slpqeoqaqys7S1tre4ubrCw8TFxsfIycrS09TV1tfY2drh4uPk5ebn6Onq8fLz9PX29/j5+v/EAB8BAAMBAQEBAQEBAQEAAAAAAAABAgMEBQYHCAkKC//EALURAAIBAgQEAwQHBQQEAAECdwABAgMRBAUhMQYSQVEHYXETIjKBCBRCkaGxwQkjM1LwFWJy0QoWJDThJfEXGBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uLj5OXm5+jp6vLz9PX29/j5+v/bAEMABgYGBgYGCgYGCg4KCgoOEg4ODg4SFxISEhISFxwXFxcXFxccHBwcHBwcHCIiIiIiIicnJycnLCwsLCwsLCwsLP/bAEMBBwcHCwoLEwoKEy4fGh8uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLi4uLv/dAAQABP/aAAwDAQACEQMRAD8A83lPGaqzn/iXgnqZB/WpWbKjNV7kgWC5/wCen9DXix3PoGtCreFJG3OcbVFZmx2XL8A9PoOa9u0b4TDVLH+0tavDZMyBkiUDKqRkGQsQBkc49O9ebeJ9Am8PXX2bzkuYJAWhmjOVcA4Pc4I7jNelCm1BOx5M6kXNpM5VnX77EEn17D6Vt6aVaNtnABxitnwn4DvPEUS3lxIIoH5HG5yPUL059zVTxLoUPhDUYGs7gzRO+yXOCB6A7eOlTUSa5U9SqbcXzNaGdenbYxhevymsPc0rGVyDg9O1a96d9uPT5RWK/C/d6ck0qK0HXd5H/9Dy2U9B2rpPCNgmp6xp9vKgeNJWmdSMgrGN3P44qponhvVvE9ybLSYw8iKXYs21VHTk+56V7B4T8F3nhSKS91gx/anHlxqjbgqty2TgcnA/KvNo0m2n0PYr1oxi431F8R3d7Jef6MbaZ964huDhSCBlsZ5OfXp2rwzxZdyS6rLC0C26xuRhCNrkHbvAHTpivUvEdrdiaWZ4DIXXarrwVJ/oQce9eZXfg3WLgNc22ySNSIzufawc9Bz6116uTucbUYwSRreFb23sLCG6v72RraFjGbVOQwOeo78HjvTtavfDdvpyRWNo4LyIx3sSTg5xz3Hfr9a4n7Bd6bfW9orxSSSyBAqncpYnGDxx161614T8JXet3/8AbXidRHZaVuxDu3FmXLMWPp+XtxQqTk9Be2UYnj94ymFB64zWSxDnJ5UenGas3bmaWRkG1Gdii+iknA/AVQKsoyRwO1ONJxVmTKrGTuj/0e3+D9iLfR5tRZcSXUu0H/ZjxjH4k165fQG4tXRADJ/Dnpn3ri/BVt9h8OaXCMf6lSw772BY/wDoVdm90qSCPHJ6VUI2gkE581RyPNdQQJKVkj3smCpYZYY6Ae+elcT43e78M+F43twI57u4+Y4B25BYgA8cYHNe3ytbtK7lFLttwcc8nHX8K8V+OF5EdK0+BOrXJP4BD/jQkrlTk7aHjPgmztp/E8FxetsgtUluZH7hYULZ+oOK7XQEsNN+G2ra/bNMLu8mNmC8hI2uwwMdCdpJJOTnPSvOdNuPI0/V5lOG+wOg/wC2ksSH9Ca7DXwNH8A6Fpak7rxpL6X6kAL+QJrVLTQwe5545Qc9u1Z104cbe1Pkl3fSqW4szj8qzbLSP//S+ghGIfJjAA2gDHpgY49qZIxN2T2Rf1NULK5XVL66u4+YLaQ20ZH8Tp/rD+BO38DUyzlndWHclT6r2rVkR3KV7eLb3cELIx8zI3DGAM/mcdT6DmvBPjZdfvNLj6bvMfHoOAP0r6JMqujxnoyH9P8A9dfK/wAZrozeILeFOTHbDA9NzMSfyAqLblyZ57arv0vUmzjbbZ/8ixj+ddd8QbxpW0W0PHk6ZASB0G8Fq86ecx2c8Y6SIqn6bg39K6TxS0pv7dpTnNjabfZREuBWqfumdtTmpG2rmqUT/vDnvU07YGKpx4EoySvuKyZZ/9k=
                BDAY;value=date:1989-01-05
                ORG:Vodafone Egypt;
                item1.EMAIL;type=INTERNET:hanyyasser@hotmail.com
                item1.X-ABLabel:INTERNET
                item2.EMAIL;type=INTERNET:hanybotbot@hotmail.com
                item2.X-ABLabel:INTERNET
                item3.ADR;type=HOME:;;Heliopolis;Cairo;Al Qahirah;;Egypt
                item4.ADR;type=HOME:;;;cairo;;;Egypt
                item5.URL:http://www.facebook.com/profile.php?id=626850952
                item5.X-ABLabel:_$!<HomePage>!$_
                X-FACEBOOK:hany.yasser1
                END:VCARD
            </vcard>
        </media>
    </message>
    '''


    def __init__(self, name, card_data, _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None):

        super(VCardMediaMessageProtocolEntity, self).__init__("vcard", _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setVcardMediaProps(name,card_data)

    def __str__(self):
        out  = super(MediaMessageProtocolEntity, self).__str__()
        out += "Name: %s\n" % self.name
        out += "Card Data: %s\n" % self.card_data
        return out

    def getName(self):
        return self.name

    def getCardData(self):
        return self.card_data

    def setVcardMediaProps(self, name, card_data):
        self.name = name
        self.card_data = card_data

    def toProtocolTreeNode(self):
        node = super(VCardMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("enc")
        mediaNode["type"] = "vcard"
        vcardNode = ProtocolTreeNode("vcard", {"name":self.name}, None,self.card_data)
        mediaNode.addChild(vcardNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = VCardMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setVcardMediaProps(
            mediaNode.getAllChildren()[0].getAttributeValue('name'),
            mediaNode.getChild("vcard").getData()
        )
        return entity
