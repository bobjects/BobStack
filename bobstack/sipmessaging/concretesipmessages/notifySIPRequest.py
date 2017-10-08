from ...sipmessaging import SIPRequest


class NOTIFYSIPRequest(SIPRequest):
    @property
    def is_notify_request(self):
        return True

    @property
    def is_known(self):
        return True
