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

    def nextForString(self, aString):
        if SIPRequestStartLine.canMatchString(aString):
            return SIPRequestStartLine.newParsedFrom(aString)
        elif SIPResponseStartLine.canMatchString(aString):
            return SIPResponseStartLine.newParsedFrom(aString)
        else:
            return MalformedSIPStartLine.newParsedFrom(aString)

