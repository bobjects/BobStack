# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipRequestStartLine import SIPRequestStartLine
from sipResponseStartLine import SIPResponseStartLine
from malformedSIPStartLine import MalformedSIPStartLine


class SIPStartLineFactory(object):
    def __init__(self):
        pass

    def nextForStringIO(self, aStringIO):
        lineString = aStringIO.readline().rstrip('\r\n')
        return self.nextForString(lineString)

    def nextForString(self, aString):
        if SIPRequestStartLine.canParseString(aString):
            return SIPRequestStartLine(aString)
        elif SIPResponseStartLine.canParseString(aString):
            return SIPResponseStartLine(aString)
        else:
            return MalformedSIPStartLine(aString)

