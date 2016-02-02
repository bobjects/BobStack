# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from malformedSIPStartLine import MalformedSIPStartLine
from sipRequestStartLine import SIPRequestStartLine
from sipResponseStartLine import SIPResponseStartLine
from sipResponse import SIPResponse
from unknownSIPRequest import UnknownSIPRequest
from malformedSIPMessage import MalformedSIPMessage
from eventSourceMixin import EventSourceMixin


class SIPMessageFactory(EventSourceMixin):
    def __init__(self):
        EventSourceMixin.__init__(self)

    def nextPutAll(self, aString):
        stringIO = StringIO(aString)
        firstLine = stringIO.readline().rstrip('\r\n')
        stringIO.close()
        sipStartLine = self.sipStartLineClassForString(firstLine)(firstLine)
        sipMessage = self.sipMessageClassForStartLine(sipStartLine)(aString, sipStartLine)
        self.triggerEventForSIPMessage(sipMessage)
        return sipMessage

    # TODO:  This is copied / pasted in SIPMessage.  Refactor into a factory.
    def sipStartLineClassForString(self, aString):
        if SIPRequestStartLine.canParseString(aString):
            return SIPRequestStartLine
        elif SIPResponseStartLine.canParseString(aString):
            return SIPResponseStartLine
        else:
            return MalformedSIPStartLine

    def sipMessageClassForStartLine(self, aSIPStartLine):
        # TODO:  this will get fleshed out as we define SIP messages.
        if aSIPStartLine.isRequest:
            if True:
                return UnknownSIPRequest
            else:
                return UnknownSIPRequest
        elif aSIPStartLine.isResponse:
            return SIPResponse
        else:
            return MalformedSIPMessage

    def triggerEventForSIPMessage(self, aSIPMessage):
        if aSIPMessage.isMalformed:
            self.triggerEvent("malformedSIPMessage")
        if aSIPMessage.isValid:
            self.triggerEvent("validSIPMessage")
            if aSIPMessage.isKnown:
                self.triggerEvent("validKnownSIPMessage")
            else:
                self.triggerEvent("validUnknownSIPMessage")
        else:
            self.triggerEvent("invalidSIPMessage")
