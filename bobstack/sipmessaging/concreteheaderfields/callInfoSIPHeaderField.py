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


class CallInfoSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Call-Info'

    @classmethod
    def newForAttributes(cls, field_name="Call-Info", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isCallInfo(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def m(self):
        return self.parameterNamed('m')

    @m.setter
    def m(self, a_string):
        self.parameterNamedPut('m', a_string)

    @property
    def purpose(self):
        return self.parameterNamed('purpose')

    @purpose.setter
    def purpose(self, a_string):
        self.parameterNamedPut('purpose', a_string)
