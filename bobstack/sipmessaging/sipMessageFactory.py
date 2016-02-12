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
from concretesipmessages import ACKSIPRequest
from concretesipmessages import BYESIPRequest
from concretesipmessages import CANCELSIPRequest
from concretesipmessages import INFOSIPRequest
from concretesipmessages import INVITESIPRequest
from concretesipmessages import NOTIFYSIPRequest
from concretesipmessages import OPTIONSSIPRequest
from concretesipmessages import REFERSIPRequest
from concretesipmessages import REGISTERSIPRequest
from concretesipmessages import SUBSCRIBESIPRequest
from concretesipmessages import UPDATESIPRequest
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
        if aSIPStartLine.isRequest:
            return {
                'ACK': ACKSIPRequest,
                'BYE': BYESIPRequest,
                'CANCEL': CANCELSIPRequest,
                'INFO': INFOSIPRequest,
                'INVITE': INVITESIPRequest,
                'NOTIFY': NOTIFYSIPRequest,
                'OPTIONS': OPTIONSSIPRequest,
                'REFER': REFERSIPRequest,
                'REGISTER': REGISTERSIPRequest,
                'SUBSCRIBE': SUBSCRIBESIPRequest,
                'UPDATE': UPDATESIPRequest
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
