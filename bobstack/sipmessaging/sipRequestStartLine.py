try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine
from classproperty import classproperty


# TODO: We need to make request_uri first class, not a string.  Do that soon, including changing a plethora of tests.

class SIPRequestStartLine(SIPStartLine):
    @classmethod
    def new_for_attributes(cls, sip_method="", request_uri=""):
        answer = cls()
        answer.sip_method = sip_method
        answer.request_uri = request_uri
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._sipMethod = None
        self._requestURI = None

    @property
    def sip_method(self):
        if self._sipMethod is None:
            self.parse_attributes_from_raw_string()
        return self._sipMethod

    @sip_method.setter
    def sip_method(self, a_string):
        self._sipMethod = a_string
        self.clear_raw_string()

    @property
    def request_uri(self):
        if self._requestURI is None:
            self.parse_attributes_from_raw_string()
        return self._requestURI

    @request_uri.setter
    def request_uri(self, a_string):
        self._requestURI = a_string
        self.clear_raw_string()

    def clear_attributes(self):
        self._sipMethod = None
        self._requestURI = None

    def parse_attributes_from_raw_string(self):
        self._sipMethod = ""
        self._requestURI = ""
        match = self.__class__.regex_for_parsing.match(self._rawString)
        if match:
            self._sipMethod, self._requestURI = match.group(1, 2)

    def render_raw_string_from_attributes(self):
        stringio = StringIO()
        stringio.write(str(self._sipMethod))
        stringio.write(" ")
        stringio.write(str(self._requestURI))
        stringio.write(" SIP/2.0")
        self._rawString = stringio.getvalue()
        stringio.close()

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regex_for_matching(cls):
        return cls.regex_for_parsing

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regex_for_parsing(cls):
        try:
            return cls._regexForParsing
        except AttributeError:
            cls._regexForParsing = re.compile('^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$')
            return cls._regexForParsing

    @classmethod
    def can_match_string(cls, a_string):
        return cls.regex_for_matching.match(a_string) is not None

    @property
    def is_request(self):
        return True

