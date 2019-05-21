class MessageMetaAttributes(object):
    def __init__(
            self, id=None, sender=None, recipient=None, notify=None, timestamp=None, participant=None, offline=None,
            retry=None
    ):
        assert (sender or recipient), "Must specify either sender or recipient " \
                                      "jid to create the message "
        assert not (sender and recipient), "Can't set both attributes to message at same " \
                                           "time (sender, recipient) "
        self.id = id
        self.sender = sender
        self.recipient = recipient
        self.notify = notify
        self.timestamp = int(timestamp) if timestamp else None
        self.participant = participant
        self.offline = offline in ("1", True)
        self.retry = int(retry) if retry else None

    @staticmethod
    def from_message_protocoltreenode(node):
        return MessageMetaAttributes(
            node["id"], node["from"], node["to"], node["notify"], node["t"], node["participant"], node["offline"],
            node["retry"]
        )
