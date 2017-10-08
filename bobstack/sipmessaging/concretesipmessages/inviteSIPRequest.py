# import sys
# sys.path.append("../../..")
# from ..sipmessaging import SIPRequest
from ...sipmessaging import SIPRequest


class INVITESIPRequest(SIPRequest):
    @property
    def is_invite_request(self):
        return True

    @property
    def is_known(self):
        return True
