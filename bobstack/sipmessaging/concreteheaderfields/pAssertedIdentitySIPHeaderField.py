try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import SIPHeaderField
from sipmessaging import classproperty


class PAssertedIdentitySIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'P-Asserted-Identity'

    @classmethod
    def newForAttributes(cls, field_name="P-Asserted-Identity", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isPAssertedIdentity(self):
        return True

