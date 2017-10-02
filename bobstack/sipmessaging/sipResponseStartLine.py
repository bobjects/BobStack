try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from sipStartLine import SIPStartLine
from classproperty import classproperty


class SIPResponseStartLine(SIPStartLine):
    @classmethod
    def new_for_attributes(cls, status_code="", reason_phrase=""):
        answer = cls()
        answer.status_code = status_code
        answer.reason_phrase = reason_phrase
        return answer

    def __init__(self):
        SIPStartLine.__init__(self)
        self._statusCode = None
        self._reasonPhrase = None

    @property
    def status_code(self):
        if self._statusCode is None:
            self.parse_attributes_from_raw_string()
        return self._statusCode

    @status_code.setter
    def status_code(self, a_string):
        self._statusCode = a_string
        self.clear_raw_string()

    @property
    def reason_phrase(self):
        if self._reasonPhrase is None:
            self.parse_attributes_from_raw_string()
        return self._reasonPhrase

    @reason_phrase.setter
    def reason_phrase(self, a_string):
        self._reasonPhrase = a_string
        self.clear_raw_string()

    def clear_attributes(self):
        self._statusCode = None
        self._reasonPhrase = None

    def parse_attributes_from_raw_string(self):
        self._statusCode = 500
        self._reasonPhrase = ""
        match = self.__class__.regex_for_parsing.match(self._rawString)
        if match:
            self._statusCode, self._reasonPhrase = match.group(1, 2)
            self._statusCode = int(self._statusCode)

    def render_raw_string_from_attributes(self):
        stringio = StringIO()
        stringio.write("SIP/2.0 ")
        stringio.write(str(self._statusCode))
        stringio.write(" ")
        stringio.write(str(self._reasonPhrase))
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
            cls._regexForParsing = re.compile("^SIP/2.0\s+([\d]+)+\s+(.+)\s*$")
            return cls._regexForParsing

    @classmethod
    def can_match_string(cls, a_string):
        return cls.regex_for_matching.match(a_string) is not None

    @property
    def is_response(self):
        return True

    # TODO:  need to test.
    @property
    def is_provisional(self):
        # True if 1xx
        return self.status_code.startsWith('1')

    # TODO:  need to test.
    @property
    def is_final(self):
        return not self.is_provisional
