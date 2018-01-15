class ConnectionCallbacks(object):
    def onConnected(self):
        pass

    def onDisconnected(self):
        pass

    def onRecvData(self, data):
        pass

    def onConnecting(self):
        pass

    def onConnectionError(self, error):
        pass


class YowConnectionDispatcher(object):
    def __init__(self, connectionCallbacks):
        assert isinstance(connectionCallbacks, ConnectionCallbacks)
        self.connectionCallbacks = connectionCallbacks

    def connect(self, host):
        pass

    def disconnect(self):
        pass

    def sendData(self, data):
        pass