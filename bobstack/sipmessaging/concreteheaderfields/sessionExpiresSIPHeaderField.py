try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField


class SessionExpiresSIPHeaderField(IntegerSIPHeaderField):
    @classmethod
    def canonicalFieldName(cls):
        return 'Session-Expires'

    @property
    def isSessionExpires(self):
        return True

