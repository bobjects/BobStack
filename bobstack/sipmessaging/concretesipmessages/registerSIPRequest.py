# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPRequest
from ...sipmessaging import SIPRequest


class REGISTERSIPRequest(SIPRequest):
    @property
    def is_register_request(self):
        return True

    @property
    def is_known(self):
        return True
