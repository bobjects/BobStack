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
        sipMessage = self.sipMessageClassForStartLine(sipStartLine).newParsedFrom(aString)
        self.triggerEventForSIPMessage(sipMessage)
        return sipMessage

    def sipMessageClassForStartLine(self, aSIPStartLine):
        # TODO:  this will get fleshed out as we define SIP messages.
        if aSIPStartLine.isRequest:
            return {
                'OPTIONS': OPTIONSSIPRequest
            }.get(aSIPStartLine.sipMethod, UnknownSIPRequest)
            # if aSIPStartLine.sipMethod == 'OPTIONS':
            #     return OPTIONSSIPRequest
            # else:
            #     return UnknownSIPRequest
        elif aSIPStartLine.isResponse:
            return SIPResponse
        else:
            return MalformedSIPMessage

    def triggerEventForSIPMessage(self, aSIPMessage):
        if aSIPMessage.isMalformed:
            self.triggerEvent("malformedSIPMessage", aSIPMessage)
        if aSIPMessage.isValid:
            self.triggerEvent("validSIPMessage", aSIPMessage)
            if aSIPMessage.isKnown:
                self.triggerEvent("validKnownSIPMessage", aSIPMessage)
            else:
                self.triggerEvent("validUnknownSIPMessage", aSIPMessage)
        else:
            self.triggerEvent("invalidSIPMessage", aSIPMessage)
