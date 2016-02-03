# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# from malformedSIPStartLine import MalformedSIPStartLine
# from sipRequestStartLine import SIPRequestStartLine
# from sipResponseStartLine import SIPResponseStartLine
from sipStartLineFactory import SIPStartLineFactory
from sipResponse import SIPResponse
from optionsSIPRequest import OPTIONSSIPRequest
from unknownSIPRequest import UnknownSIPRequest
from malformedSIPMessage import MalformedSIPMessage
from eventSourceMixin import EventSourceMixin


class SIPMessageFactory(EventSourceMixin):
    def __init__(self):
        EventSourceMixin.__init__(self)

    def nextForString(self, aString):
        stringIO = StringIO(aString)
        sipStartLine = SIPStartLineFactory().nextForStringIO(stringIO)
        stringIO.close()
        sipMessage = self.sipMessageClassForStartLine(sipStartLine)(aString, sipStartLine)
        self.triggerEventForSIPMessage(sipMessage)
        return sipMessage

    def sipMessageClassForStartLine(self, aSIPStartLine):
        # TODO:  this will get fleshed out as we define SIP messages.
        # TODO:  use a dictionary instead of a if elif else.
        if aSIPStartLine.isRequest:
            if aSIPStartLine.sipMethod == 'OPTIONS':
                return OPTIONSSIPRequest
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
