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


class AuthorizationSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalFieldName(cls):
        return 'Authorization'

    @classmethod
    def newForAttributes(cls, fieldName="Authorization", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isAuthorization(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameterNamed('algorithm')

    @algorithm.setter
    def algorithm(self, aString):
        self.parameterNamedPut('algorithm', aString)

    @property
    def auts(self):
        return self.parameterNamed('auts')

    @auts.setter
    def auts(self, aString):
        self.parameterNamedPut('auts', aString)

    @property
    def cnonce(self):
        return self.parameterNamed('cnonce')

    @cnonce.setter
    def cnonce(self, aString):
        self.parameterNamedPut('cnonce', aString)

    @property
    def nc(self):
        return self.parameterNamed('nc')

    @nc.setter
    def nc(self, aString):
        self.parameterNamedPut('nc', aString)

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
    def response(self):
        return self.parameterNamed('response')

    @response.setter
    def response(self, aString):
        self.parameterNamedPut('response', aString)

    @property
    def uri(self):
        return self.parameterNamed('uri')

    @uri.setter
    def uri(self, aString):
        self.parameterNamedPut('uri', aString)

    @property
    def username(self):
        return self.parameterNamed('username')

    @username.setter
    def username(self, aString):
        self.parameterNamedPut('username', aString)


