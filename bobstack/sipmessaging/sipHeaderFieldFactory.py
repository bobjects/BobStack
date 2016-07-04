try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import re
from classproperty import classproperty
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
from concreteheaderfields import SubjectSIPHeaderField
from concreteheaderfields import ReferredBySIPHeaderField
from concreteheaderfields import ReferToSIPHeaderField
from concreteheaderfields import AllowEventsSIPHeaderField
from concreteheaderfields import EventSIPHeaderField
from concreteheaderfields import ContentEncodingSIPHeaderField
from concreteheaderfields import RAckSIPHeaderField
from concreteheaderfields import PChargeSIPHeaderField
from concreteheaderfields import ReplyToSIPHeaderField
from concreteheaderfields import UnsupportedSIPHeaderField
from concreteheaderfields import PAssertedIdentitySIPHeaderField
from concreteheaderfields import PPreferredIdentitySIPHeaderField
from concreteheaderfields import RemotePartyIDSIPHeaderField
from concreteheaderfields import AlertInfoSIPHeaderField
from concreteheaderfields import HistoryInfoSIPHeaderField
from concreteheaderfields import PCalledPartyIdSIPHeaderField
from concreteheaderfields import PRTPStatSIPHeaderField
from concreteheaderfields import PrivacySIPHeaderField
from concreteheaderfields import ProxyAuthenticateSIPHeaderField
from concreteheaderfields import ProxyAuthorizationSIPHeaderField
from concreteheaderfields import ProxyRequireSIPHeaderField
from concreteheaderfields import ReasonSIPHeaderField
from concreteheaderfields import RecordSessionExpiresSIPHeaderField
from concreteheaderfields import ReplacesSIPHeaderField
from concreteheaderfields import SubscriptionStateSIPHeaderField
from concreteheaderfields import MinExpiresSIPHeaderField
from unknownSIPHeaderField import UnknownSIPHeaderField


class SIPHeaderFieldFactory(object):
    headerFieldNamesAndClasses = {
        'content-length': ContentLengthSIPHeaderField,
        'content-length:': ContentLengthSIPHeaderField,
        'l': ContentLengthSIPHeaderField,
        'l:': ContentLengthSIPHeaderField,
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
        'i': CallIDSIPHeaderField,
        'i:': CallIDSIPHeaderField,
        'call-info': CallInfoSIPHeaderField,
        'call-info:': CallInfoSIPHeaderField,
        'contact': ContactSIPHeaderField,
        'contact:': ContactSIPHeaderField,
        'm': ContactSIPHeaderField,
        'm:': ContactSIPHeaderField,
        'content-disposition': ContentDispositionSIPHeaderField,
        'content-disposition:': ContentDispositionSIPHeaderField,
        'content-type': ContentTypeSIPHeaderField,
        'content-type:': ContentTypeSIPHeaderField,
        'c': ContentTypeSIPHeaderField,
        'c:': ContentTypeSIPHeaderField,
        'date': DateSIPHeaderField,
        'date:': DateSIPHeaderField,
        'expires': ExpiresSIPHeaderField,
        'expires:': ExpiresSIPHeaderField,
        'from': FromSIPHeaderField,
        'from:': FromSIPHeaderField,
        'f': FromSIPHeaderField,
        'f:': FromSIPHeaderField,
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
        'k': SupportedSIPHeaderField,
        'k:': SupportedSIPHeaderField,
        'timestamp': TimestampSIPHeaderField,
        'timestamp:': TimestampSIPHeaderField,
        'to': ToSIPHeaderField,
        'to:': ToSIPHeaderField,
        't': ToSIPHeaderField,
        't:': ToSIPHeaderField,
        'user-agent': UserAgentSIPHeaderField,
        'user-agent:': UserAgentSIPHeaderField,
        'www-authenticate': WWWAuthenticateSIPHeaderField,
        'www-authenticate:': WWWAuthenticateSIPHeaderField,
        'warning': WarningSIPHeaderField,
        'warning:': WarningSIPHeaderField,
        'via': ViaSIPHeaderField,
        'via:': ViaSIPHeaderField,
        'v': ViaSIPHeaderField,
        'v:': ViaSIPHeaderField,
        'subject': SubjectSIPHeaderField,
        'subject:': SubjectSIPHeaderField,
        's': SubjectSIPHeaderField,
        's:': SubjectSIPHeaderField,
        'referred-by': ReferredBySIPHeaderField,
        'referred-by:': ReferredBySIPHeaderField,
        'b': ReferredBySIPHeaderField,
        'b:': ReferredBySIPHeaderField,
        'refer-to': ReferToSIPHeaderField,
        'refer-to:': ReferToSIPHeaderField,
        'r': ReferToSIPHeaderField,
        'r:': ReferToSIPHeaderField,
        'allow-events': AllowEventsSIPHeaderField,
        'allow-events:': AllowEventsSIPHeaderField,
        'u': AllowEventsSIPHeaderField,
        'u:': AllowEventsSIPHeaderField,
        'event': EventSIPHeaderField,
        'event:': EventSIPHeaderField,
        'o': EventSIPHeaderField,
        'o:': EventSIPHeaderField,
        'content-encoding': ContentEncodingSIPHeaderField,
        'content-encoding:': ContentEncodingSIPHeaderField,
        'e': ContentEncodingSIPHeaderField,
        'e:': ContentEncodingSIPHeaderField,
        'rack': RAckSIPHeaderField,
        'rack:': RAckSIPHeaderField,
        'p-charge': PChargeSIPHeaderField,
        'p-charge:': PChargeSIPHeaderField,
        'reply-to': ReplyToSIPHeaderField,
        'reply-to:': ReplyToSIPHeaderField,
        'unsupported': UnsupportedSIPHeaderField,
        'unsupported:': UnsupportedSIPHeaderField,
        'p-asserted-identity': PAssertedIdentitySIPHeaderField,
        'p-asserted-identity:': PAssertedIdentitySIPHeaderField,
        'p-preferred-identity': PPreferredIdentitySIPHeaderField,
        'p-preferred-identity:': PPreferredIdentitySIPHeaderField,
        'remote-party-id': RemotePartyIDSIPHeaderField,
        'remote-party-id:': RemotePartyIDSIPHeaderField,
        'alert-info': AlertInfoSIPHeaderField,
        'alert-info:': AlertInfoSIPHeaderField,
        'history-info': HistoryInfoSIPHeaderField,
        'history-info:': HistoryInfoSIPHeaderField,
        'p-called-party-id': PCalledPartyIdSIPHeaderField,
        'p-called-party-id:': PCalledPartyIdSIPHeaderField,
        'p-rtp-stat': PRTPStatSIPHeaderField,
        'p-rtp-stat:': PRTPStatSIPHeaderField,
        'privacy': PrivacySIPHeaderField,
        'privacy:': PrivacySIPHeaderField,
        'proxy-authenticate': ProxyAuthenticateSIPHeaderField,
        'proxy-authenticate:': ProxyAuthenticateSIPHeaderField,
        'proxy-authorization': ProxyAuthorizationSIPHeaderField,
        'proxy-authorization:': ProxyAuthorizationSIPHeaderField,
        'proxy-require': ProxyRequireSIPHeaderField,
        'proxy-require:': ProxyRequireSIPHeaderField,
        'reason': ReasonSIPHeaderField,
        'reason:': ReasonSIPHeaderField,
        'record-session-expires': RecordSessionExpiresSIPHeaderField,
        'record-session-expires:': RecordSessionExpiresSIPHeaderField,
        'replaces': ReplacesSIPHeaderField,
        'replaces:': ReplacesSIPHeaderField,
        'subscription-state': SubscriptionStateSIPHeaderField,
        'subscription-state:': SubscriptionStateSIPHeaderField,
        'min-expires': MinExpiresSIPHeaderField,
        'min-expires:': MinExpiresSIPHeaderField,
    }

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def regexForGettingHeaderFieldName(cls):
        try:
            return cls._regexForGettingHeaderFieldName
        except AttributeError:
            cls._regexForGettingHeaderFieldName = re.compile('^([^\s:]*)')
            return cls._regexForGettingHeaderFieldName

    def allForStringIO(self, aStringIO):
        lineStrings = []
        lineString = aStringIO.readline().rstrip('\r\n')
        while lineString:
            # lineStrings.append(lineString)
            if lineString.startswith((' ', '\t')) and lineStrings:
                # line folding!
                lineStrings[-1] += lineString
            else:
                lineStrings.append(lineString)

            lineString = aStringIO.readline().rstrip('\r\n')
        return [self.nextForString(s) for s in lineStrings]

    def classForString(self, aString):
        # This is invalid.  There can be no whitespace before the colon.
        # try:
        #     return self.classForFieldName(aString.split()[0])
        # except IndexError:
        #     return UnknownSIPHeaderField
        match = self.__class__.regexForGettingHeaderFieldName.match(aString)
        if match:
            return self.classForFieldName(match.group(1))
        else:
            return UnknownSIPHeaderField

    def classForFieldName(self, aString):
        return self.__class__.headerFieldNamesAndClasses.get(aString.lower(), UnknownSIPHeaderField)

    def nextForString(self, aString):
        return self.classForString(aString).newParsedFrom(aString)

    def nextForFieldName(self, aString):
        return self.classForFieldName(aString).newForFieldNameAndValueString(fieldName=aString)

    def nextForFieldNameAndFieldValue(self, fieldName, fieldValueString):
        return self.classForFieldName(fieldName).newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)
