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
from concretesipmessages import PRACKSIPRequest
from concretesipmessages import PUBLISHSIPRequest
from concretesipmessages import MESSAGESIPRequest
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
        'PRACK': PRACKSIPRequest,
        'PUBLISH': PUBLISHSIPRequest,
        'MESSAGE': MESSAGESIPRequest,
        'OPTIONS': OPTIONSSIPRequest,
        'REFER': REFERSIPRequest,
        'REGISTER': REGISTERSIPRequest,
        'SUBSCRIBE': SUBSCRIBESIPRequest,
        'UPDATE': UPDATESIPRequest
    }

    def __init__(self):
        EventSourceMixin.__init__(self)

    def nextForString(self, a_string):
        string_io = StringIO(a_string)
        sipStartLine = SIPStartLineFactory().nextForStringIO(string_io)
        string_io.close()
        sipMessage = self.sipMessageClassForStartLine(sipStartLine).newParsedFrom(a_string)
        self.triggerEventForSIPMessage(sipMessage)
        return sipMessage

    def sipMessageClassForStartLine(self, a_sip_start_line):
        if a_sip_start_line.isRequest:
            return self.__class__.methodNamesAndClasses.get(a_sip_start_line.sip_method, UnknownSIPRequest)
        elif a_sip_start_line.isResponse:
            return SIPResponse
        else:
            return MalformedSIPMessage

    def triggerEventForSIPMessage(self, a_sip_message):
        self.triggerEvent("sipMessage", a_sip_message)
        if a_sip_message.isRequest:
            self.triggerEvent("sipRequest", a_sip_message)
            if a_sip_message.isValid:
                self.triggerEvent("validSIPRequest", a_sip_message)
            else:
                self.triggerEvent("invalidSIPRequest", a_sip_message)
        if a_sip_message.isResponse:
            self.triggerEvent("sipResponse", a_sip_message)
            if a_sip_message.isValid:
                self.triggerEvent("validSIPResponse", a_sip_message)
            else:
                self.triggerEvent("invalidSIPResponse", a_sip_message)
        if a_sip_message.isMalformed:
            self.triggerEvent("malformedSIPMessage", a_sip_message)
        if a_sip_message.isValid:
            self.triggerEvent("validSIPMessage", a_sip_message)
            if a_sip_message.isKnown:
                self.triggerEvent("validKnownSIPMessage", a_sip_message)
            else:
                self.triggerEvent("validUnknownSIPMessage", a_sip_message)
        else:
            self.triggerEvent("invalidSIPMessage", a_sip_message)
