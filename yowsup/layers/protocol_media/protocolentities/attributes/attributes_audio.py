class AudioAttributes(object):
    def __init__(self, seconds, ptt):
        """
        :param seconds: duration of audio playback in seconds
        :type seconds: int
        :param ptt: indicates whether this is a push-to-talk audio message
        :type ptt: bool
        """
        self._seconds = seconds  # type: int
        self._ptt = ptt  # type: bool

    @property
    def seconds(self):
        return self._seconds

    @property
    def ptt(self):
        return self._ptt
