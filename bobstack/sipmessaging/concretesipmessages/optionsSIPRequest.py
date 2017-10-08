from ...sipmessaging import SIPRequest


class OPTIONSSIPRequest(SIPRequest):
    @property
    def is_options_request(self):
        return True

    @property
    def is_known(self):
        return True
