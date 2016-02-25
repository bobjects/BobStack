try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from concreteheaderfields import ContentLengthSIPHeaderField
from concreteheaderfields import ViaSIPHeaderField
from concreteheaderfields import AcceptSIPHeaderField
from concreteheaderfields import AcceptEncodingSIPHeaderField
from concreteheaderfields import AcceptLanguageSIPHeaderField
from concreteheaderfields import AllowSIPHeaderField
from concreteheaderfields import AuthorizationSIPHeaderField
from concreteheaderfields import CSeqSIPHeaderField
from concreteheaderfields import CallIDSIPHeaderField
from concreteheaderfields import CallInfoSIPHeaderField
from concreteheaderfields import ContactSIPHeaderField
from concreteheaderfields import ContentDispositionSIPHeaderField
from concreteheaderfields import ContentTypeSIPHeaderField
from concreteheaderfields import DateSIPHeaderField
from concreteheaderfields import ExpiresSIPHeaderField
from concreteheaderfields import FromSIPHeaderField
from concreteheaderfields import MaxForwardsSIPHeaderField
from concreteheaderfields import RecordRouteSIPHeaderField
from concreteheaderfields import RequireSIPHeaderField
from concreteheaderfields import RetryAfterSIPHeaderField
from concreteheaderfields import RouteSIPHeaderField
from concreteheaderfields import ServerSIPHeaderField
from concreteheaderfields import SessionExpiresSIPHeaderField
from concreteheaderfields import SupportedSIPHeaderField
from concreteheaderfields import TimestampSIPHeaderField
from concreteheaderfields import ToSIPHeaderField
from concreteheaderfields import UserAgentSIPHeaderField
from concreteheaderfields import WWWAuthenticateSIPHeaderField
from concreteheaderfields import WarningSIPHeaderField
from unknownSIPHeaderField import UnknownSIPHeaderField


class SIPHeaderFieldFactory(object):
    headerFieldNamesAndClasses = {
            'content-length': ContentLengthSIPHeaderField,
            'content-length:': ContentLengthSIPHeaderField,
            'accept': AcceptSIPHeaderField,
            'accept:': AcceptSIPHeaderField,
            'accept-encoding': AcceptEncodingSIPHeaderField,
            'accept-encoding:': AcceptEncodingSIPHeaderField,
            'accept-language': AcceptLanguageSIPHeaderField,
            'accept-language:': AcceptLanguageSIPHeaderField,
            'allow': AllowSIPHeaderField,
            'allow:': AllowSIPHeaderField,
            'authorization': AuthorizationSIPHeaderField,
            'authorization:': AuthorizationSIPHeaderField,
            'cseq': CSeqSIPHeaderField,
            'cseq:': CSeqSIPHeaderField,
            'call-id': CallIDSIPHeaderField,
            'call-id:': CallIDSIPHeaderField,
            'call-info': CallInfoSIPHeaderField,
            'call-info:': CallInfoSIPHeaderField,
            'contact': ContactSIPHeaderField,
            'contact:': ContactSIPHeaderField,
            'content-disposition': ContentDispositionSIPHeaderField,
            'content-disposition:': ContentDispositionSIPHeaderField,
            'content-type': ContentTypeSIPHeaderField,
            'content-type:': ContentTypeSIPHeaderField,
            'date': DateSIPHeaderField,
            'date:': DateSIPHeaderField,
            'expires': ExpiresSIPHeaderField,
            'expires:': ExpiresSIPHeaderField,
            'from': FromSIPHeaderField,
            'from:': FromSIPHeaderField,
            'max-forwards': MaxForwardsSIPHeaderField,
            'max-forwards:': MaxForwardsSIPHeaderField,
            'record-route': RecordRouteSIPHeaderField,
            'record-route:': RecordRouteSIPHeaderField,
            'require': RequireSIPHeaderField,
            'require:': RequireSIPHeaderField,
            'retry-after': RetryAfterSIPHeaderField,
            'retry-after:': RetryAfterSIPHeaderField,
            'route': RouteSIPHeaderField,
            'route:': RouteSIPHeaderField,
            'server': ServerSIPHeaderField,
            'server:': ServerSIPHeaderField,
            'session-expires': SessionExpiresSIPHeaderField,
            'session-expires:': SessionExpiresSIPHeaderField,
            'supported': SupportedSIPHeaderField,
            'supported:': SupportedSIPHeaderField,
            'timestamp': TimestampSIPHeaderField,
            'timestamp:': TimestampSIPHeaderField,
            'to': ToSIPHeaderField,
            'to:': ToSIPHeaderField,
            'user-agent': UserAgentSIPHeaderField,
            'user-agent:': UserAgentSIPHeaderField,
            'www-authenticate': WWWAuthenticateSIPHeaderField,
            'www-authenticate:': WWWAuthenticateSIPHeaderField,
            'warning': WarningSIPHeaderField,
            'warning:': WarningSIPHeaderField,
            'via': ViaSIPHeaderField,
            'via:': ViaSIPHeaderField,
        }

    def allForStringIO(self, aStringIO):
        answer = []
        lineString = aStringIO.readline().rstrip('\r\n')
        while lineString:
            answer.append(self.nextForString(lineString))
            lineString = aStringIO.readline().rstrip('\r\n')
        return answer

    def classForString(self, aString):
        try:
            return self.classForFieldName(aString.split()[0])
        except IndexError:
            return UnknownSIPHeaderField

    def classForFieldName(self, aString):
        return self.__class__.headerFieldNamesAndClasses.get(aString.lower(), UnknownSIPHeaderField)

    def nextForString(self, aString):
        return self.classForString(aString).newParsedFrom(aString)

    def nextForFieldName(self, aString):
        return self.classForFieldName(aString).newForFieldAttributes(fieldName=aString)

    def nextForFieldNameAndFieldValue(self, fieldName, fieldValue):
        return self.classForFieldName(fieldName).newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
