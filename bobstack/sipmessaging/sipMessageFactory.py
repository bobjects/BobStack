# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
from malformedSIPStartLine import MalformedSIPStartLine
from sipRequestStartLine import SIPRequestStartLine
from sipResponseStartLine import SIPResponseStartLine
from unknownSIPRequest import UnknownSIPRequest
from unknownSIPResponse import UnknownSIPResponse
from malformedSIPMessage import MalformedSIPMessage


class SIPMessageFactory(object):
    def __init__(self):
        # TODO
        pass

    def nextPutAll(self, aString):
        # TODO
        pass

    def sipStartLineClassForString(self, aString):
        if SIPRequestStartLine.matchesLine(aString):
            return SIPRequestStartLine
        elif SIPRequestStartLine.matchesLine(aString):
            return SIPResponseStartLine
        else:
            return MalformedSIPStartLine

    def sipMessageClassForStartLine(self, aSIPStartLine):
        # TODO:  this will get fleshed out as we defined SIP messages.
        if aSIPStartLine.isRequest:
            if True:
                return UnknownSIPRequest
            else:
                return UnknownSIPRequest
        elif aSIPStartLine.isResponse:
            if True:
                return UnknownSIPResponse
            else:
                return UnknownSIPResponse
        else:
            return MalformedSIPMessage