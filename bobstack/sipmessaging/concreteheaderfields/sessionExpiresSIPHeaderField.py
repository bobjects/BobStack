try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
import sys
sys.path.append("../../..")
from bobstack.sipmessaging import IntegerSIPHeaderField
from bobstack.sipmessaging import classproperty

# TODO:  We must be able to parse out refresher parameter, e.g.:  "1200;refresher=uac"
# See https://tools.ietf.org/html/rfc4028
# Do we want to allow for Integer headers to parse out params generally?  For right now, just
# do it here, but I would bet that other integer headers will need that as well.

class SessionExpiresSIPHeaderField(IntegerSIPHeaderField):
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Session-Expires'

    @property
    def isSessionExpires(self):
        return True

