class SymmetricAxolotlParameters:
    def __init__(self, ourBaseKey, ourRatchetKey,
                 ourIdentityKey, theirBaseKey,
                 theirRatchetKey, theirIdentityKey):
        """
        :type ourBaseKey: ECKeyPair
        :type ourRatchetKey: ECKeyPair
        :type ourIdentityKey: IdentityKeyPair
        :type theirBaseKey: ECPublicKey
        :type theirRatchetKey: ECKeyPair
        :type theirIdentityKey: IdentityKey
        """

        self.ourBaseKey = ourBaseKey
        self.ourIdentityKey = ourIdentityKey
        self.ourRatchetKey = ourRatchetKey
        self.theirRatchetKey = theirRatchetKey
        self.theirIdentityKey = theirIdentityKey
        self.theirBaseKey = theirBaseKey

        if ourBaseKey is None or ourIdentityKey is None or ourRatchetKey is None\
            or theirRatchetKey is None or theirIdentityKey is None or theirBaseKey is None:
            raise Exception("Null value!")

    def getOurBaseKey(self):
        return self.ourBaseKey

    def getOurIdentityKey(self):
        return self.ourIdentityKey

    def getTheirRatchetKey(self):
        return self.theirRatchetKey

    def getTheirIdentityKey(self):
        return self.theirIdentityKey

    def getTheirBaseKey(self):
        return self.theirBaseKey

    def getOurRatchetKey(self):
        return self.ourRatchetKey

    @staticmethod
    def newBuilder():
        return SymmetricAxolotlParameters.Builder()

    class Builder:
        def __init__(self):
            self.ourIdentityKey = None
            self.ourBaseKey = None
            self.ourRatchetKey = None
            self.theirRatchetKey = None
            self.theirIdentityKey = None
            self.theirBaseKey = None

        def setOurIdentityKey(self, ourIdentityKey):
            self.ourIdentityKey = ourIdentityKey
            return self

        def setOurBaseKey(self, ourBaseKey):
            self.ourBaseKey = ourBaseKey
            return self

        def setOurRatchetKey(self, ourRatchetKey):
            self.ourRatchetKey = ourRatchetKey
            return self

        def setTheirRatchetKey(self, theirRatchetKey):
            self.theirRatchetKey = theirRatchetKey
            return self



        def setTheirIdentityKey(self, theirIdentityKey):
            self.theirIdentityKey = theirIdentityKey
            return self

        def setTheirBaseKey(self, theirBaseKey):
            self.theirBaseKey = theirBaseKey
            return self

        def create(self):
            return SymmetricAxolotlParameters(self.ourBaseKey, self.ourRatchetKey, self.ourIdentityKey,
                                        self.theirBaseKey, self.theirRatchetKey, self.theirIdentityKey)