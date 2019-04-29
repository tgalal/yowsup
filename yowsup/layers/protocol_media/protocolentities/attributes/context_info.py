class ContextInfo(object):
    def __init__(self,
                 stanza_id=None,
                 participant=None,
                 quoted_message=None,
                 remote_jid=None,
                 mentioned_jid=None,
                 edit_version=None,
                 revoke_message=None
                 ):
        self._stanza_id= stanza_id
        self._participant = participant
        self._quoted_message = quoted_message
        self._remote_jid = remote_jid
        self._mentioned_jid = mentioned_jid
        self._edit_version = edit_version
        self._revoke_message = revoke_message

    @property
    def stanza_id(self):
        return self._stanza_id

    @property
    def participant(self):
        return self._participant

    @property
    def quoted_message(self):
        return self._quoted_message

    @property
    def remote_jid(self):
        return self._remote_jid

    @property
    def mentioned_jid(self):
        return self._mentioned_jid

    @property
    def edit_version(self):
        return self._edit_version

    @property
    def revoke_message(self):
        return self._revoke_message
