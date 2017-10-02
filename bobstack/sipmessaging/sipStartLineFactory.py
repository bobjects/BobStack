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
    def next_for_stringio(self, a_stringio):
        line_string = a_stringio.readline().rstrip('\r\n')
        return self.next_for_string(line_string)

    @staticmethod
    def next_for_string(a_string):
        if SIPRequestStartLine.can_match_string(a_string):
            return SIPRequestStartLine.new_parsed_from(a_string)
        elif SIPResponseStartLine.can_match_string(a_string):
            return SIPResponseStartLine.new_parsed_from(a_string)
        else:
            return MalformedSIPStartLine.new_parsed_from(a_string)

