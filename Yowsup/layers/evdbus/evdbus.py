from Yowsup import YowLayer
import dbus


YS_BUSNAME = 'org.openwa.Yowsup'
YS_IFACE = 'org.openwa.Yowsup'

class YowDBusLayer(YowLayer, dbus.service.Object):
 
    def __init__(self):
        YowLayer.__init__(self)
        dbus.service.Object.__init__(self)
        self.bus = dbus.SessionBus()

    def init(self):
        self.initUpper()

    def send(self, data):
        self.toLower(data)

    def receive(self, data):
        self.toUpper(data)

    #dbus methods

    @dbus.service.method(interface = dbus.PROPERTIES_IFACE,
                         in_signature='ss', out_signature='v')
    def Get(self, interface_name, property_name):
        return self.GetAll(interface_name)[property_name]

    @dbus.service.method(interface = YS_IFACE, in_signature = "ss", out_signature = "v")
    def login(self, username, password):
        print "SHOULD LOGIN"