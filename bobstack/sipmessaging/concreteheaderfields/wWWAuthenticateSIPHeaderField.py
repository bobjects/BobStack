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
    def newForAttributes(cls, field_name="WWW-Authenticate", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isWWWAuthenticate(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def algorithm(self):
        return self.parameterNamed('algorithm')

    @algorithm.setter
    def algorithm(self, a_string):
        self.parameterNamedPut('algorithm', a_string)

    @property
    def domain(self):
        return self.parameterNamed('domain')

    @domain.setter
    def domain(self, a_string):
        self.parameterNamedPut('domain', a_string)

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
    def stale(self):
        return self.parameterNamed('stale')

    @stale.setter
    def stale(self, a_string):
        self.parameterNamedPut('stale', a_string)
