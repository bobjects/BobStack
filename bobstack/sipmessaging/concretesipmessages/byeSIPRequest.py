from ...sipmessaging import SIPRequest


class BYESIPRequest(SIPRequest):
    @property
    def is_bye_request(self):
        return True

    @property
    def is_known(self):
        return True
