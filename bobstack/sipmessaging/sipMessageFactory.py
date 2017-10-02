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

    def next_for_string(self, a_string):
        string_io = StringIO(a_string)
        sip_start_line = SIPStartLineFactory().next_for_stringio(string_io)
        string_io.close()
        sip_message = self.sip_message_class_for_start_line(sip_start_line).new_parsed_from(a_string)
        self.trigger_event_for_sip_message(sip_message)
        return sip_message

    def sip_message_class_for_start_line(self, a_sip_start_line):
        if a_sip_start_line.is_request:
            return self.__class__.methodNamesAndClasses.get(a_sip_start_line.sip_method, UnknownSIPRequest)
        elif a_sip_start_line.is_response:
            return SIPResponse
        else:
            return MalformedSIPMessage

    def trigger_event_for_sip_message(self, a_sip_message):
        self.trigger_event("sipMessage", a_sip_message)
        if a_sip_message.is_request:
            self.trigger_event("sipRequest", a_sip_message)
            if a_sip_message.is_valid:
                self.trigger_event("validSIPRequest", a_sip_message)
            else:
                self.trigger_event("invalidSIPRequest", a_sip_message)
        if a_sip_message.is_response:
            self.trigger_event("sipResponse", a_sip_message)
            if a_sip_message.is_valid:
                self.trigger_event("validSIPResponse", a_sip_message)
            else:
                self.trigger_event("invalidSIPResponse", a_sip_message)
        if a_sip_message.is_malformed:
            self.trigger_event("malformedSIPMessage", a_sip_message)
        if a_sip_message.is_valid:
            self.trigger_event("validSIPMessage", a_sip_message)
            if a_sip_message.is_known:
                self.trigger_event("validKnownSIPMessage", a_sip_message)
            else:
                self.trigger_event("validUnknownSIPMessage", a_sip_message)
        else:
            self.trigger_event("invalidSIPMessage", a_sip_message)
