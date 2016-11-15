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


class WWWAuthenticateSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'WWW-Authenticate'

    @classmethod
    def newForAttributes(cls, fieldName="WWW-Authenticate", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isWWWAuthenticate(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameterNamed('algorithm')

    @algorithm.setter
    def algorithm(self, aString):
        self.parameterNamedPut('algorithm', aString)

    @property
    def domain(self):
        return self.parameterNamed('domain')

    @domain.setter
    def domain(self, aString):
        self.parameterNamedPut('domain', aString)

    @property
    def nonce(self):
        return self.parameterNamed('nonce')

    @nonce.setter
    def nonce(self, aString):
        self.parameterNamedPut('nonce', aString)

    @property
    def opaque(self):
        return self.parameterNamed('opaque')

    @opaque.setter
    def opaque(self, aString):
        self.parameterNamedPut('opaque', aString)

    @property
    def qop(self):
        return self.parameterNamed('qop')

    @qop.setter
    def qop(self, aString):
        self.parameterNamedPut('qop', aString)

    @property
    def realm(self):
        return self.parameterNamed('realm')

    @realm.setter
    def realm(self, aString):
        self.parameterNamedPut('realm', aString)

    @property
    def stale(self):
        return self.parameterNamed('stale')

    @stale.setter
    def stale(self, aString):
        self.parameterNamedPut('stale', aString)
