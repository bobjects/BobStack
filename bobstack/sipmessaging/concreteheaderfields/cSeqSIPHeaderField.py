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


class CSeqSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'CSeq'

    @classmethod
    def new_for_attributes(cls, field_name="CSeq", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_cseq(self):
        return True

