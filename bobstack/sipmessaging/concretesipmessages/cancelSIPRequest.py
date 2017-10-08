from ...sipmessaging import SIPRequest


class CANCELSIPRequest(SIPRequest):
    @property
    def is_cancel_request(self):
        return True

    @property
    def is_known(self):
        return True
