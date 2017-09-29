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
    def newForAttributes(cls, field_name="Authorization", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isAuthorization(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameterNamed('algorithm')

    @algorithm.setter
    def algorithm(self, a_string):
        self.parameterNamedPut('algorithm', a_string)

    @property
    def auts(self):
        return self.parameterNamed('auts')

    @auts.setter
    def auts(self, a_string):
        self.parameterNamedPut('auts', a_string)

    @property
    def cnonce(self):
        return self.parameterNamed('cnonce')

    @cnonce.setter
    def cnonce(self, a_string):
        self.parameterNamedPut('cnonce', a_string)

    @property
    def nc(self):
        return self.parameterNamed('nc')

    @nc.setter
    def nc(self, a_string):
        self.parameterNamedPut('nc', a_string)

    @property
    def nonce(self):
        return self.parameterNamed('nonce')

    @nonce.setter
    def nonce(self, a_string):
        self.parameterNamedPut('nonce', a_string)

    @property
    def opaque(self):
        return self.parameterNamed('opaque')

    @opaque.setter
    def opaque(self, a_string):
        self.parameterNamedPut('opaque', a_string)

    @property
    def qop(self):
        return self.parameterNamed('qop')

    @qop.setter
    def qop(self, a_string):
        self.parameterNamedPut('qop', a_string)

    @property
    def realm(self):
        return self.parameterNamed('realm')

    @realm.setter
    def realm(self, a_string):
        self.parameterNamedPut('realm', a_string)

    @property
    def response(self):
        return self.parameterNamed('response')

    @response.setter
    def response(self, a_string):
        self.parameterNamedPut('response', a_string)

    @property
    def uri(self):
        return self.parameterNamed('uri')

    @uri.setter
    def uri(self, a_string):
        self.parameterNamedPut('uri', a_string)

    @property
    def username(self):
        return self.parameterNamed('username')

    @username.setter
    def username(self, a_string):
        self.parameterNamedPut('username', a_string)


