from yowsup.layers.protocol_media.protocolentities.attributes.context_info import ContextInfo


class MediaAttributes(object):
    def __init__(self, context_info=None):
        """
        :type context_info: ContextInfo | None
        """
        if context_info:
            assert type(context_info) is ContextInfo
        self._context_info = context_info  # type: ContextInfo | None

    @property
    def context_info(self):
        return self._context_info
