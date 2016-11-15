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
    def newForAttributes(cls, fieldName="Call-Info", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isCallInfo(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def m(self):
        return self.parameterNamed('m')

    @m.setter
    def m(self, aString):
        self.parameterNamedPut('m', aString)

    @property
    def purpose(self):
        return self.parameterNamed('purpose')

    @purpose.setter
    def purpose(self, aString):
        self.parameterNamedPut('purpose', aString)
