try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
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
    methodNamesAndClasses = {
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
    }

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
            return self.__class__.methodNamesAndClasses.get(aSIPStartLine.sipMethod, UnknownSIPRequest)
        elif aSIPStartLine.isResponse:
            return SIPResponse
        else:
            return MalformedSIPMessage

    def triggerEventForSIPMessage(self, aSIPMessage):
        self.triggerEvent("sipMessage", aSIPMessage)
        if aSIPMessage.isRequest:
            self.triggerEvent("sipRequest", aSIPMessage)
            if aSIPMessage.isValid:
                self.triggerEvent("validSIPRequest", aSIPMessage)
            else:
                self.triggerEvent("invalidSIPRequest", aSIPMessage)
        if aSIPMessage.isResponse:
            self.triggerEvent("sipResponse", aSIPMessage)
            if aSIPMessage.isValid:
                self.triggerEvent("validSIPResponse", aSIPMessage)
            else:
                self.triggerEvent("invalidSIPResponse", aSIPMessage)
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
