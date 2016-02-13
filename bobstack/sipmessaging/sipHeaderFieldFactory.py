# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# from contentLengthSIPHeaderField import ContentLengthSIPHeaderField
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
    def allForStringIO(self, aStringIO):
        headerFieldLines = []
        lineString = aStringIO.readline().rstrip('\r\n')
        while lineString.__len__() > 0:
            headerFieldLines.append(lineString)
            lineString = aStringIO.readline().rstrip('\r\n')
        return [self.nextForString(line) for line in headerFieldLines]

    def nextForString(self, aString):
        # TODO:  Do we want to do something more elegant than a big elif thing?
        if ContentLengthSIPHeaderField.canMatchString(aString):
            return ContentLengthSIPHeaderField.newParsedFrom(aString)
        elif ViaSIPHeaderField.canMatchString(aString):
            return ViaSIPHeaderField.newParsedFrom(aString)
        elif AcceptSIPHeaderField.canMatchString(aString):
            return AcceptSIPHeaderField.newParsedFrom(aString)
        elif AcceptEncodingSIPHeaderField.canMatchString(aString):
            return AcceptEncodingSIPHeaderField.newParsedFrom(aString)
        elif AcceptLanguageSIPHeaderField.canMatchString(aString):
            return AcceptLanguageSIPHeaderField.newParsedFrom(aString)
        elif AllowSIPHeaderField.canMatchString(aString):
            return AllowSIPHeaderField.newParsedFrom(aString)
        elif AuthorizationSIPHeaderField.canMatchString(aString):
            return AuthorizationSIPHeaderField.newParsedFrom(aString)
        elif CSeqSIPHeaderField.canMatchString(aString):
            return CSeqSIPHeaderField.newParsedFrom(aString)
        elif CallIDSIPHeaderField.canMatchString(aString):
            return CallIDSIPHeaderField.newParsedFrom(aString)
        elif CallInfoSIPHeaderField.canMatchString(aString):
            return CallInfoSIPHeaderField.newParsedFrom(aString)
        elif ContactSIPHeaderField.canMatchString(aString):
            return ContactSIPHeaderField.newParsedFrom(aString)
        elif ContentDispositionSIPHeaderField.canMatchString(aString):
            return ContentDispositionSIPHeaderField.newParsedFrom(aString)
        elif ContentTypeSIPHeaderField.canMatchString(aString):
            return ContentTypeSIPHeaderField.newParsedFrom(aString)
        elif DateSIPHeaderField.canMatchString(aString):
            return DateSIPHeaderField.newParsedFrom(aString)
        elif ExpiresSIPHeaderField.canMatchString(aString):
            return ExpiresSIPHeaderField.newParsedFrom(aString)
        elif FromSIPHeaderField.canMatchString(aString):
            return FromSIPHeaderField.newParsedFrom(aString)
        elif MaxForwardsSIPHeaderField.canMatchString(aString):
            return MaxForwardsSIPHeaderField.newParsedFrom(aString)
        elif RecordRouteSIPHeaderField.canMatchString(aString):
            return RecordRouteSIPHeaderField.newParsedFrom(aString)
        elif RequireSIPHeaderField.canMatchString(aString):
            return RequireSIPHeaderField.newParsedFrom(aString)
        elif RetryAfterSIPHeaderField.canMatchString(aString):
            return RetryAfterSIPHeaderField.newParsedFrom(aString)
        elif RouteSIPHeaderField.canMatchString(aString):
            return RouteSIPHeaderField.newParsedFrom(aString)
        elif ServerSIPHeaderField.canMatchString(aString):
            return ServerSIPHeaderField.newParsedFrom(aString)
        elif SessionExpiresSIPHeaderField.canMatchString(aString):
            return SessionExpiresSIPHeaderField.newParsedFrom(aString)
        elif SupportedSIPHeaderField.canMatchString(aString):
            return SupportedSIPHeaderField.newParsedFrom(aString)
        elif TimestampSIPHeaderField.canMatchString(aString):
            return TimestampSIPHeaderField.newParsedFrom(aString)
        elif ToSIPHeaderField.canMatchString(aString):
            return ToSIPHeaderField.newParsedFrom(aString)
        elif UserAgentSIPHeaderField.canMatchString(aString):
            return UserAgentSIPHeaderField.newParsedFrom(aString)
        elif WWWAuthenticateSIPHeaderField.canMatchString(aString):
            return WWWAuthenticateSIPHeaderField.newParsedFrom(aString)
        elif WarningSIPHeaderField.canMatchString(aString):
            return WarningSIPHeaderField.newParsedFrom(aString)
        else:
            return UnknownSIPHeaderField.newParsedFrom(aString)

    def nextForFieldName(self, aString):
        if ContentLengthSIPHeaderField.canMatchFieldName(aString):
            return ContentLengthSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ViaSIPHeaderField.canMatchFieldName(aString):
            return ViaSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif AcceptSIPHeaderField.canMatchFieldName(aString):
            return AcceptSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif AcceptEncodingSIPHeaderField.canMatchFieldName(aString):
            return AcceptEncodingSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif AcceptLanguageSIPHeaderField.canMatchFieldName(aString):
            return AcceptLanguageSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif AllowSIPHeaderField.canMatchFieldName(aString):
            return AllowSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif AuthorizationSIPHeaderField.canMatchFieldName(aString):
            return AuthorizationSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif CSeqSIPHeaderField.canMatchFieldName(aString):
            return CSeqSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif CallIDSIPHeaderField.canMatchFieldName(aString):
            return CallIDSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif CallInfoSIPHeaderField.canMatchFieldName(aString):
            return CallInfoSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ContactSIPHeaderField.canMatchFieldName(aString):
            return ContactSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ContentDispositionSIPHeaderField.canMatchFieldName(aString):
            return ContentDispositionSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ContentTypeSIPHeaderField.canMatchFieldName(aString):
            return ContentTypeSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif DateSIPHeaderField.canMatchFieldName(aString):
            return DateSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ExpiresSIPHeaderField.canMatchFieldName(aString):
            return ExpiresSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif FromSIPHeaderField.canMatchFieldName(aString):
            return FromSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif MaxForwardsSIPHeaderField.canMatchFieldName(aString):
            return MaxForwardsSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif RecordRouteSIPHeaderField.canMatchFieldName(aString):
            return RecordRouteSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif RequireSIPHeaderField.canMatchFieldName(aString):
            return RequireSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif RetryAfterSIPHeaderField.canMatchFieldName(aString):
            return RetryAfterSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif RouteSIPHeaderField.canMatchFieldName(aString):
            return RouteSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ServerSIPHeaderField.canMatchFieldName(aString):
            return ServerSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif SessionExpiresSIPHeaderField.canMatchFieldName(aString):
            return SessionExpiresSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif SupportedSIPHeaderField.canMatchFieldName(aString):
            return SupportedSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif TimestampSIPHeaderField.canMatchFieldName(aString):
            return TimestampSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif ToSIPHeaderField.canMatchFieldName(aString):
            return ToSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif UserAgentSIPHeaderField.canMatchFieldName(aString):
            return UserAgentSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif WWWAuthenticateSIPHeaderField.canMatchFieldName(aString):
            return WWWAuthenticateSIPHeaderField.newForFieldAttributes(fieldName=aString)
        elif WarningSIPHeaderField.canMatchFieldName(aString):
            return WarningSIPHeaderField.newForFieldAttributes(fieldName=aString)
        else:
            return UnknownSIPHeaderField.newParsedFrom(aString)

    def nextForFieldNameAndFieldValue(self, fieldName, fieldValue):
        if ContentLengthSIPHeaderField.canMatchFieldName(fieldName):
            return ContentLengthSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ViaSIPHeaderField.canMatchFieldName(fieldName):
            return ViaSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif AcceptSIPHeaderField.canMatchFieldName(fieldName):
            return AcceptSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif AcceptEncodingSIPHeaderField.canMatchFieldName(fieldName):
            return AcceptEncodingSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif AcceptLanguageSIPHeaderField.canMatchFieldName(fieldName):
            return AcceptLanguageSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif AllowSIPHeaderField.canMatchFieldName(fieldName):
            return AllowSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif AuthorizationSIPHeaderField.canMatchFieldName(fieldName):
            return AuthorizationSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif CSeqSIPHeaderField.canMatchFieldName(fieldName):
            return CSeqSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif CallIDSIPHeaderField.canMatchFieldName(fieldName):
            return CallIDSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif CallInfoSIPHeaderField.canMatchFieldName(fieldName):
            return CallInfoSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ContactSIPHeaderField.canMatchFieldName(fieldName):
            return ContactSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ContentDispositionSIPHeaderField.canMatchFieldName(fieldName):
            return ContentDispositionSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ContentTypeSIPHeaderField.canMatchFieldName(fieldName):
            return ContentTypeSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif DateSIPHeaderField.canMatchFieldName(fieldName):
            return DateSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ExpiresSIPHeaderField.canMatchFieldName(fieldName):
            return ExpiresSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif FromSIPHeaderField.canMatchFieldName(fieldName):
            return FromSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif MaxForwardsSIPHeaderField.canMatchFieldName(fieldName):
            return MaxForwardsSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif RecordRouteSIPHeaderField.canMatchFieldName(fieldName):
            return RecordRouteSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif RequireSIPHeaderField.canMatchFieldName(fieldName):
            return RequireSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif RetryAfterSIPHeaderField.canMatchFieldName(fieldName):
            return RetryAfterSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif RouteSIPHeaderField.canMatchFieldName(fieldName):
            return RouteSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ServerSIPHeaderField.canMatchFieldName(fieldName):
            return ServerSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif SessionExpiresSIPHeaderField.canMatchFieldName(fieldName):
            return SessionExpiresSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif SupportedSIPHeaderField.canMatchFieldName(fieldName):
            return SupportedSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif TimestampSIPHeaderField.canMatchFieldName(fieldName):
            return TimestampSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ToSIPHeaderField.canMatchFieldName(fieldName):
            return ToSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif UserAgentSIPHeaderField.canMatchFieldName(fieldName):
            return UserAgentSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif WWWAuthenticateSIPHeaderField.canMatchFieldName(fieldName):
            return WWWAuthenticateSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif WarningSIPHeaderField.canMatchFieldName(fieldName):
            return WarningSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        else:
            return UnknownSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

