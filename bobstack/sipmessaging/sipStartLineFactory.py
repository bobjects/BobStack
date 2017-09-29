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
    def nextForStringIO(self, aStringIO):
        lineString = aStringIO.readline().rstrip('\r\n')
        return self.nextForString(lineString)

    @staticmethod
    def nextForString(a_string):
        if SIPRequestStartLine.canMatchString(a_string):
            return SIPRequestStartLine.newParsedFrom(a_string)
        elif SIPResponseStartLine.canMatchString(a_string):
            return SIPResponseStartLine.newParsedFrom(a_string)
        else:
            return MalformedSIPStartLine.newParsedFrom(a_string)

