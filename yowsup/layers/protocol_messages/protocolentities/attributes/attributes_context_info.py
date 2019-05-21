class ContextInfoAttributes(object):
    def __init__(self,
                 stanza_id=None,
                 participant=None,
                 quoted_message=None,
                 remote_jid=None,
                 mentioned_jid=None,
                 edit_version=None,
                 revoke_message=None
                 ):
        self._stanza_id = stanza_id
        self._participant = participant
        self._quoted_message = quoted_message
        self._remote_jid = remote_jid
        self._mentioned_jid = mentioned_jid or []
        self._edit_version = edit_version
        self._revoke_message = revoke_message

    def __str__(self):
        attribs = []
        if self._stanza_id is not None:
            attribs.append(("stanza_id", self.stanza_id))
        if self._participant is not None:
            attribs.append(("participant", self.participant))
        if self.quoted_message is not None:
            attribs.append(("quoted_message", self.quoted_message))
        if self._remote_jid is not None:
            attribs.append(("remote_jid", self.remote_jid))
        if self.mentioned_jid is not None and len(self.mentioned_jid):
            attribs.append(("mentioned_jid", self.mentioned_jid))
        if self.edit_version is not None:
            attribs.append(("edit_version", self.edit_version))
        if self.revoke_message is not None:
            attribs.append(("revoke_message", self.revoke_message))

        return "[%s]" % " ".join((map(lambda item: "%s=%s" % item, attribs)))

    @property
    def stanza_id(self):
        return self._stanza_id

    @stanza_id.setter
    def stanza_id(self, value):
        self._stanza_id = value

    @property
    def participant(self):
        return self._participant

    @participant.setter
    def participant(self, value):
        self._participant = value

    @property
    def quoted_message(self):
        return self._quoted_message

    @quoted_message.setter
    def quoted_message(self, value):
        self._quoted_message = value

    @property
    def remote_jid(self):
        return self._remote_jid

    @remote_jid.setter
    def remote_jid(self, value):
        self._remote_jid = value

    @property
    def mentioned_jid(self):
        return self._mentioned_jid

    @mentioned_jid.setter
    def mentioned_jid(self, value):
        self._mentioned_jid = value

    @property
    def edit_version(self):
        return self._edit_version

    @edit_version.setter
    def edit_version(self, value):
        self._edit_version = value

    @property
    def revoke_message(self):
        return self._revoke_message

    @revoke_message.setter
    def revoke_message(self, value):
        self._revoke_message = value
