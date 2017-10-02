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
    def canonical_field_name(cls):
        return 'Authorization'

    @classmethod
    def new_for_attributes(cls, field_name="Authorization", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_authorization(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameter_named('algorithm')

    @algorithm.setter
    def algorithm(self, a_string):
        self.parameter_named_put('algorithm', a_string)

    @property
    def auts(self):
        return self.parameter_named('auts')

    @auts.setter
    def auts(self, a_string):
        self.parameter_named_put('auts', a_string)

    @property
    def cnonce(self):
        return self.parameter_named('cnonce')

    @cnonce.setter
    def cnonce(self, a_string):
        self.parameter_named_put('cnonce', a_string)

    @property
    def nc(self):
        return self.parameter_named('nc')

    @nc.setter
    def nc(self, a_string):
        self.parameter_named_put('nc', a_string)

    @property
    def nonce(self):
        return self.parameter_named('nonce')

    @nonce.setter
    def nonce(self, a_string):
        self.parameter_named_put('nonce', a_string)

    @property
    def opaque(self):
        return self.parameter_named('opaque')

    @opaque.setter
    def opaque(self, a_string):
        self.parameter_named_put('opaque', a_string)

    @property
    def qop(self):
        return self.parameter_named('qop')

    @qop.setter
    def qop(self, a_string):
        self.parameter_named_put('qop', a_string)

    @property
    def realm(self):
        return self.parameter_named('realm')

    @realm.setter
    def realm(self, a_string):
        self.parameter_named_put('realm', a_string)

    @property
    def response(self):
        return self.parameter_named('response')

    @response.setter
    def response(self, a_string):
        self.parameter_named_put('response', a_string)

    @property
    def uri(self):
        return self.parameter_named('uri')

    @uri.setter
    def uri(self, a_string):
        self.parameter_named_put('uri', a_string)

    @property
    def username(self):
        return self.parameter_named('username')

    @username.setter
    def username(self, a_string):
        self.parameter_named_put('username', a_string)


