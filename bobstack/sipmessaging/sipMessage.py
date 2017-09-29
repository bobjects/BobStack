try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeader import SIPHeader
from sipStartLineFactory import SIPStartLineFactory


class SIPMessage(object):
    @classmethod
    def newParsedFrom(cls, a_string):
        answer = cls()
        answer.rawString = a_string
        return answer

    @classmethod
    def _newForAttributes(cls, start_line=None, header=None, content=""):
        answer = cls()
        answer.start_line = start_line
        if header:
            answer.header = header
        else:
            answer.header = SIPHeader.newForAttributes(header_fields=None)
        answer.content = content
        return answer

    def __init__(self):
        self._content = None
        self._startLine = None
        self._header = None
        self._rawString = None

    @property
    def deepCopy(self):
        return self.__class__.newParsedFrom(self.rawString)

    @property
    def rawString(self):
        if self._rawString is None:
            self.renderRawStringFromAttributes()
        return self._rawString

    @rawString.setter
    def rawString(self, a_string):
        self._rawString = a_string
        self.clearAttributes()

    @property
    def body(self):
        return self.content

    def clearRawString(self):
        self._rawString = None

    def clearAttributes(self):
        self._content = None
        self._startLine = None
        self._header = None

    def parseAttributesFromRawString(self):
        self._content = ""
        string_io = StringIO(self._rawString)
        self._startLine = SIPStartLineFactory().nextForStringIO(string_io)
        self._header = SIPHeader.newParsedFrom(string_io)
        self._content = string_io.read()
        string_io.close()

    def renderRawStringFromAttributes(self):
        stringio = StringIO()
        stringio.write(self._startLine.rawString)
        stringio.write("\r\n")
        self._header.renderRawStringFromAttributes(stringio)
        stringio.write(self._content)
        self._rawString = stringio.getvalue()
        stringio.close()

    @property
    def start_line(self):
        if self._startLine is None:
            self.parseAttributesFromRawString()
        return self._startLine

    @start_line.setter
    def start_line(self, a_sip_start_line):
        self._startLine = a_sip_start_line
        self.clearRawString()

    @property
    def header(self):
        if self._header is None:
            self.parseAttributesFromRawString()
        return self._header

    @header.setter
    def header(self, a_sip_header):
        self._header = a_sip_header
        self.clearRawString()

    @property
    def content(self):
        if self._content is None:
            self.parseAttributesFromRawString()
        return self._content

    @content.setter
    def content(self, a_string):
        self._content = a_string
        self.clearRawString()

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
    def isValid(self):
        if self.isMalformed:
            return False
        if not self.header.isValid:
            return False
        if self.header.contentLength is not None:
            if self.header.contentLength != self.content.__len__():
                return False
        return True

    @property
    def isInvalid(self):
        return not self.isValid

    @property
    def isUnknown(self):
        return not self.isKnown

    @property
    def isKnown(self):
        return False

    @property
    def isMalformed(self):
        return False

    @property
    def isRequest(self):
        return False

    @property
    def isResponse(self):
        return False

    @property
    def isACKRequest(self):
        return False

    @property
    def isBYERequest(self):
        return False

    @property
    def isCANCELRequest(self):
        return False

    @property
    def isINFORequest(self):
        return False

    @property
    def isINVITERequest(self):
        return False

    @property
    def isMESSAGERequest(self):
        return False

    @property
    def isNOTIFYRequest(self):
        return False

    @property
    def isOPTIONSRequest(self):
        return False

    @property
    def isPUBLISHRequest(self):
        return False

    @property
    def isPRACKRequest(self):
        return False

    @property
    def isREFERRequest(self):
        return False

    @property
    def isREGISTERRequest(self):
        return False

    @property
    def isSUBSCRIBERequest(self):
        return False

    @property
    def isUPDATERequest(self):
        return False

