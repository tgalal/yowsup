class MessageKeyAttributes(object):
    def __init__(self, remote_jid, from_me, id, participant):
        self._remote_jid = remote_jid
        self._from_me = from_me
        self._id = id
        self._participant = participant

    def __str__(self):
        attrs = []
        if self.remote_jid is not None:
            attrs.append(("remote_jid", self.remote_jid))
        if self.from_me is not None:
            attrs.append(("from_me", self.from_me))
        if self.id is not None:
            attrs.append(("id", self.id))
        if self.participant is not None:
            attrs.append(("participant", self.participant))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attrs)))

    @property
    def remote_jid(self):
        return self._remote_jid

    @remote_jid.setter
    def remote_jid(self, value):
        self._remote_jid = value

    @property
    def from_me(self):
        return self._from_me

    @from_me.setter
    def from_me(self, value):
        self._from_me = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def participant(self):
        return self._participant

    @participant.setter
    def participant(self, value):
        self._participant = value
