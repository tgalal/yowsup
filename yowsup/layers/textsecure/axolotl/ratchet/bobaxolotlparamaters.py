class BobAxolotlParameters:

    def __init__(self, ourIdentityKey, ourSignedPreKey,
                 ourRatchetKey, ourOneTimePreKey,
                 theirIdentityKey, theirBaseKey):
        """
        :type ourIdentityKey: IdentityKeyPair
        :type ourSignedPreKey: ECKeyPair
        :type ourRatchetKey: ECKeyPair
        :type ourOneTimePreKey: ECKeyPair
        :type theirIdentityKey: IdentityKey
        :type theirBaseKey: ECPublicKey
        """

        self.ourIdentityKey = ourIdentityKey
        self.ourSignedPreKey = ourSignedPreKey
        self.ourRatchetKey = ourRatchetKey
        self.ourOneTimePreKey = ourOneTimePreKey
        self.theirIdentityKey = theirIdentityKey
        self.theirBaseKey = theirBaseKey

        if ourIdentityKey is None or ourSignedPreKey is None or ourRatchetKey is None\
            or theirIdentityKey is None or theirBaseKey is None:
            raise Exception("Null value!")

    def getOurIdentityKey(self):
        return self.ourIdentityKey

    def getOurSignedPreKey(self):
        return self.ourSignedPreKey

    def getOurOneTimePreKey(self):
        return self.ourOneTimePreKey

    def getTheirIdentityKey(self):
        return self.theirIdentityKey

    def getTheirBaseKey(self):
        return self.theirBaseKey

    def getOurRatchetKey(self):
        return self.ourRatchetKey

    @staticmethod
    def newBuilder():
        return BobAxolotlParameters.Builder()

    class Builder:
        def __init__(self):
            self.ourIdentityKey = None
            self.ourSignedPreKey = None
            self.ourOneTimePreKey = None
            self.ourRatchetKey = None
            self.theirIdentityKey = None
            self.theirBaseKey = None

        def setOurIdentityKey(self, ourIdentityKey):
            self.ourIdentityKey = ourIdentityKey
            return self

        def setOurSignedPreKey(self, ourSignedPreKey):
            self.ourSignedPreKey = ourSignedPreKey
            return self

        def setOurOneTimePreKey(self, ourOneTimePreKey):
            self.ourOneTimePreKey = ourOneTimePreKey
            return self

        def setOurRatchetKey(self, ourRatchetKey):
            self.ourRatchetKey = ourRatchetKey
            return self

        def setTheirIdentityKey(self, theirIdentityKey):
            self.theirIdentityKey =theirIdentityKey
            return self

        def setTheirBaseKey(self, theirBaseKey):
            self.theirBaseKey = theirBaseKey
            return self

        def create(self):
            return BobAxolotlParameters(self.ourIdentityKey, self.ourSignedPreKey, self.ourRatchetKey,
                                        self.ourOneTimePreKey, self.theirIdentityKey, self.theirBaseKey)



