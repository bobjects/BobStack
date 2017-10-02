try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeader import SIPHeader
from sipStartLineFactory import SIPStartLineFactory


class SIPMessage(object):
    @classmethod
    def new_parsed_from(cls, a_string):
        answer = cls()
        answer.raw_string = a_string
        return answer

    @classmethod
    def _newForAttributes(cls, start_line=None, header=None, content=""):
        answer = cls()
        answer.start_line = start_line
        if header:
            answer.header = header
        else:
            answer.header = SIPHeader.new_for_attributes(header_fields=None)
        answer.content = content
        return answer

    def __init__(self):
        self._content = None
        self._startLine = None
        self._header = None
        self._rawString = None

    @property
    def deepCopy(self):
        return self.__class__.new_parsed_from(self.raw_string)

    @property
    def raw_string(self):
        if self._rawString is None:
            self.render_raw_string_from_attributes()
        return self._rawString

    @raw_string.setter
    def raw_string(self, a_string):
        self._rawString = a_string
        self.clear_attributes()

    @property
    def body(self):
        return self.content

    def clear_raw_string(self):
        self._rawString = None

    def clear_attributes(self):
        self._content = None
        self._startLine = None
        self._header = None

    def parse_attributes_from_raw_string(self):
        self._content = ""
        string_io = StringIO(self._rawString)
        self._startLine = SIPStartLineFactory().next_for_stringio(string_io)
        self._header = SIPHeader.new_parsed_from(string_io)
        self._content = string_io.read()
        string_io.close()

    def render_raw_string_from_attributes(self):
        stringio = StringIO()
        stringio.write(self._startLine.raw_string)
        stringio.write("\r\n")
        self._header.render_raw_string_from_attributes(stringio)
        stringio.write(self._content)
        self._rawString = stringio.getvalue()
        stringio.close()

    @property
    def start_line(self):
        if self._startLine is None:
            self.parse_attributes_from_raw_string()
        return self._startLine

    @start_line.setter
    def start_line(self, a_sip_start_line):
        self._startLine = a_sip_start_line
        self.clear_raw_string()

    @property
    def header(self):
        if self._header is None:
            self.parse_attributes_from_raw_string()
        return self._header

    @header.setter
    def header(self, a_sip_header):
        self._header = a_sip_header
        self.clear_raw_string()

    @property
    def content(self):
        if self._content is None:
            self.parse_attributes_from_raw_string()
        return self._content

    @content.setter
    def content(self, a_string):
        self._content = a_string
        self.clear_raw_string()

    @property
    def vias(self):
        return self.header.vias

    @property
    def viaHeaderFields(self):
        return self.header.viaHeaderFields

    @property
    def routeURIs(self):
        return self.header.routeURIs

    @property
    def recordRouteURIs(self):
        return self.header.recordRouteURIs

    @property
    def transactionHash(self):
        return self.header.transactionHash

    @property
    def dialogHash(self):
        return self.header.dialogHash

    # TODO:  This is a hot method.  Should we cache?
    @property
    def is_valid(self):
        if self.is_malformed:
            return False
        if not self.header.is_valid:
            return False
        if self.header.content_length is not None:
            if self.header.content_length != self.content.__len__():
                return False
        return True

    @property
    def isInvalid(self):
        return not self.is_valid

    @property
    def isUnknown(self):
        return not self.is_known

    @property
    def is_known(self):
        return False

    @property
    def is_malformed(self):
        return False

    @property
    def is_request(self):
        return False

    @property
    def is_response(self):
        return False

    @property
    def is_ack_request(self):
        return False

    @property
    def is_bye_request(self):
        return False

    @property
    def is_cancel_request(self):
        return False

    @property
    def is_info_request(self):
        return False

    @property
    def is_invite_request(self):
        return False

    @property
    def is_message_request(self):
        return False

    @property
    def is_notify_request(self):
        return False

    @property
    def is_options_request(self):
        return False

    @property
    def is_publish_request(self):
        return False

    @property
    def is_prack_request(self):
        return False

    @property
    def is_refer_request(self):
        return False

    @property
    def is_register_request(self):
        return False

    @property
    def is_subscribe_request(self):
        return False

    @property
    def is_update_request(self):
        return False

