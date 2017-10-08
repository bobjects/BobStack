try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from ...sipmessaging import IntegerSIPHeaderField
from ...sipmessaging import classproperty


# TODO:  We must be able to parse out refresher parameter, e.g.:  "1200;refresher=uac"
# See https://tools.ietf.org/html/rfc4028
# Do we want to allow for Integer headers to parse out params generally?  For right now, just
# do it here, but I would bet that other integer headers will need that as well.
class SessionExpiresSIPHeaderField(IntegerSIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Session-Expires'

    @property
    def is_session_expires(self):
        return True

