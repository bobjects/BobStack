# from stringBuffer import StringBuffer
# from protoSIPMessage import ProtoSIPMessage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
# from contentLengthSIPHeaderField import ContentLengthSIPHeaderField
from concreteheaderfields import ContentLengthSIPHeaderField
from concreteheaderfields import ViaSIPHeaderField
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
        # TODO - this will get fleshed out as we define more header fields.
        else:
            return UnknownSIPHeaderField.newParsedFrom(aString)

    def nextForFieldName(self, aString):
        if ContentLengthSIPHeaderField.canMatchFieldName(aString):
            return ContentLengthSIPHeaderField.newForAttributes()
        elif ViaSIPHeaderField.canMatchFieldName(aString):
            return ViaSIPHeaderField.newForAttributes()
        # TODO - this will get fleshed out as we define more header fields.
        else:
            return UnknownSIPHeaderField.newParsedFrom(aString)

    def nextForFieldNameAndFieldValue(self, fieldName, fieldValue):
        if ContentLengthSIPHeaderField.canMatchFieldName(fieldName):
            return ContentLengthSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        elif ViaSIPHeaderField.canMatchFieldName(fieldName):
            return ViaSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)
        # TODO - this will get fleshed out as we define more header fields.
        else:
            return UnknownSIPHeaderField.newForFieldAttributes(fieldName=fieldName, fieldValue=fieldValue)

