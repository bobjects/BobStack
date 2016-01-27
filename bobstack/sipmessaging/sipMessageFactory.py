# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
from cStringIO import StringIO
from malformedSIPStartLine import MalformedSIPStartLine
from sipRequestStartLine import SIPRequestStartLine
from sipResponseStartLine import SIPResponseStartLine
from unknownSIPRequest import UnknownSIPRequest
from unknownSIPResponse import UnknownSIPResponse
from malformedSIPMessage import MalformedSIPMessage
from eventSourceMixin import EventSourceMixin

class SIPMessageFactory(EventSourceMixin):
    def __init__(self):
        # TODO
        pass

    def nextPutAll(self, aString):
        # TODO:  SIP messages are terminted by CRLF.  does readline strip both the CR and LF?  That's what we want.
        with StringIO(aString) as stringIO:
            firstLine = stringIO.readline()
        sipStartLine = self.sipStartLineClassForString(firstLine)(firstLine)
        sipMessage = self.sipMessageClassForStartLine(sipStartLine)(aString, sipStartLine)
        self.triggerEventForSIPMessage(sipMessage)
        return sipMessage

    def sipStartLineClassForString(self, aString):
        if SIPRequestStartLine.matchesLine(aString):
            return SIPRequestStartLine
        elif SIPRequestStartLine.matchesLine(aString):
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
            if True:
                return UnknownSIPResponse
            else:
                return UnknownSIPResponse
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
