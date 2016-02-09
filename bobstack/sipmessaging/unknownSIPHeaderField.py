try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeaderField import SIPHeaderField


class UnknownSIPHeaderField(SIPHeaderField):
    @property
    def isKnown(self):
        return False
