from ...sipmessaging import SIPRequest


class PUBLISHSIPRequest(SIPRequest):
    @property
    def is_publish_request(self):
        return True

    @property
    def is_known(self):
        return True
