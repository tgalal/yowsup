class AliceAxolotlParameters:
    def __init__(self,ourIdentityKey, ourBaseKey,
                 theirIdentityKey, theirSignedPreKey,
                  theirRatchetKey, theirOneTimePreKey):
        """
        :type ourBaseKey: ECKeyPair
        :type theirSignedPreKey: ECKeyPair
        :type ourIdentityKey: IdentityKeyPair
        :type theirOneTimePreKey: ECPublicKey
        :type theirRatchetKey: ECKeyPair
        :type theirIdentityKey: IdentityKey
        """

        self.ourBaseKey = ourBaseKey
        self.ourIdentityKey = ourIdentityKey
        self.theirSignedPreKey = theirSignedPreKey
        self.theirRatchetKey = theirRatchetKey
        self.theirIdentityKey = theirIdentityKey
        self.theirOneTimePreKey = theirOneTimePreKey

        if ourBaseKey is None or ourIdentityKey is None or theirSignedPreKey is None\
            or theirRatchetKey is None or theirIdentityKey is None or theirSignedPreKey is None:
            raise Exception("Null value!")


    def getOurIdentityKey(self):
        return self.ourIdentityKey

    def getOurBaseKey(self):
        return self.ourBaseKey

    def getTheirIdentityKey(self):
        return self.theirIdentityKey

    def getTheirSignedPreKey(self):
        return self.theirSignedPreKey


    def getTheirOneTimePreKey(self):
        return self.theirOneTimePreKey

    def getTheirRatchetKey(self):
        return self.theirRatchetKey

    @staticmethod
    def newBuilder():
        return AliceAxolotlParameters.Builder()

    class Builder:
        def __init__(self):
            self.ourIdentityKey = None
            self.ourBaseKey = None
            self.theirIdentityKey = None
            self.theirSignedPreKey = None
            self.theirRatchetKey = None
            self.theirOneTimePreKey = None

        def setOurIdentityKey(self, ourIdentityKey):
            self.ourIdentityKey = ourIdentityKey
            return self

        def setOurBaseKey(self, ourBaseKey):
            self.ourBaseKey = ourBaseKey
            return self


        def setTheirRatchetKey(self, theirRatchetKey):
            self.theirRatchetKey = theirRatchetKey
            return self

        def setTheirIdentityKey(self, theirIdentityKey):
            self.theirIdentityKey = theirIdentityKey
            return self

        def setTheirSignedPreKey(self, theirSignedPreKey):
            self.theirSignedPreKey = theirSignedPreKey
            return self


        def setTheirOneTimePreKey(self, theirOneTimePreKey):
            self.theirOneTimePreKey = theirOneTimePreKey
            return self

        def create(self):
            return AliceAxolotlParameters(self.ourIdentityKey, self.ourBaseKey, self.theirIdentityKey,
                                          self.theirSignedPreKey, self.theirRatchetKey, self.theirOneTimePreKey)