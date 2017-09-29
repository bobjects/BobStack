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


class PRTPStatSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'P-RTP-Stat'

    @classmethod
    def newForAttributes(cls, field_name="P-RTP-Stat", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isPRTPStat(self):
        return True

