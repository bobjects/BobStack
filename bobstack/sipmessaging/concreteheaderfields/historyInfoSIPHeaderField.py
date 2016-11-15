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


class HistoryInfoSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'History-Info'

    @classmethod
    def newForAttributes(cls, fieldName="History-Info", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isHistoryInfo(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def mp(self):
        return self.parameterNamed('mp')

    @mp.setter
    def mp(self, aString):
        self.parameterNamedPut('mp', aString)

    @property
    def np(self):
        return self.parameterNamed('np')

    @np.setter
    def np(self, aString):
        self.parameterNamedPut('np', aString)

    @property
    def rc(self):
        return self.parameterNamed('rc')

    @rc.setter
    def rc(self, aString):
        self.parameterNamedPut('rc', aString)
