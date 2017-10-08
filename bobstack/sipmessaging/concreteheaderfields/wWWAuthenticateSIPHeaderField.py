try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPHeaderField
# from ..sipmessaging import classproperty
from ...sipmessaging import SIPHeaderField
from ...sipmessaging import classproperty


class WWWAuthenticateSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'WWW-Authenticate'

    @classmethod
    def new_for_attributes(cls, field_name="WWW-Authenticate", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_www_authenticate(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameter_named('algorithm')

    @algorithm.setter
    def algorithm(self, a_string):
        self.parameter_named_put('algorithm', a_string)

    @property
    def domain(self):
        return self.parameter_named('domain')

    @domain.setter
    def domain(self, a_string):
        self.parameter_named_put('domain', a_string)

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
    def stale(self):
        return self.parameter_named('stale')

    @stale.setter
    def stale(self, a_string):
        self.parameter_named_put('stale', a_string)
