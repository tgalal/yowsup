class YowMessage:
    def __init__(self, _id, _from, _timestamp, _notify):
        self._id = _timestamp#_id.split('-')[0]
        self._from = _from
        self._timestamp = _timestamp
        self._notify = _notify

    def getId(self):
        return self._id

    def getFrom(self):
        return self._from

    def getTimestamp(self):
        return self._timestamp

    def getNotify(self):
        return self._notify

