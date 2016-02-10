try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from collections import OrderedDict
from sipHeaderFieldFactory import SIPHeaderFieldFactory


class SIPHeader(object):
    @classmethod
    def newParsedFrom(cls, stringioToParse):
        answer = cls()
        answer.parseAttributesFromStringIO(stringioToParse)
        return answer

    @classmethod
    def newForAttributes(cls, headerFields=None):
        answer = cls()
        if not headerFields:
            answer.headerFields = []
        else:
            answer.headerFields = headerFields
        return answer

    def __init__(self):
        self._headerFields = []
        self._knownHeaderFields = None
        self._unknownHeaderFields = None
        self._contentLengthHeaderField = None

    def parseAttributesFromStringIO(self, stringioToParse):
        self._headerFields = SIPHeaderFieldFactory().allForStringIO(stringioToParse)

    def renderRawStringFromAttributes(self, stringio):
        for headerField in self.headerFields:
            stringio.write(headerField.rawString)
            stringio.write("\r\n")
        stringio.write("\r\n")

    @property
    def contentLength(self):
        if self.contentLengthHeaderField is not None:
            return self.contentLengthHeaderField.value
        return 0

    @property
    def contentLengthHeaderField(self):
        if not self._contentLengthHeaderField:
            self._contentLengthHeaderField = next((headerField for headerField in self.headerFields if headerField.isContentLength), None)
        return self._contentLengthHeaderField

    @property
    def knownHeaderFields(self):
        if not self._knownHeaderFields:
            self._knownHeaderFields = [headerField for headerField in self.headerFields if headerField.isKnown]
        return self._knownHeaderFields

    @property
    def unknownHeaderFields(self):
        if not self._unknownHeaderFields:
            self._unknownHeaderFields = [headerField for headerField in self.headerFields if headerField.isUnknown]
        return self._unknownHeaderFields

    @property
    def isValid(self):
        return all(f.isValid for f in self.headerFields)

    @property
    def headerFields(self):
        return self._headerFields

    @headerFields.setter
    def headerFields(self, aListOrString):
        if not aListOrString:
            self._headerFields = []
        else:
            factory = SIPHeaderFieldFactory()
            if isinstance(aListOrString, list):
                if isinstance(aListOrString[0], basestring):  # list of complete header field strings
                    self._headerFields = [factory.nextForString(s) for s in aListOrString]
                elif isinstance(aListOrString[0], (list, tuple)):  # list of field names and field values
                    headerFields = []
                    for fieldName, fieldValue in aListOrString:
                        if isinstance(fieldValue, dict):  # fieldValue is dict of property names and values.
                            headerField = factory.nextForFieldName(fieldName)
                            for propertyName, propertyValue in fieldValue.iteritems():
                                prop = headerField.__class__.__dict__.get(propertyName, None)
                                if type(prop) is property:
                                    setter = prop.fset
                                    if setter:
                                        setter(headerField, propertyValue)
                            headerFields.append(headerField)
                        else:
                            headerFields.append(factory.nextForFieldNameAndFieldValue(fieldName, str(fieldValue)))
                    self._headerFields = headerFields
                else:
                    self._headerFields = aListOrString  # list of SIPHeaderField instances
            else:  # One big multiline string
                stringio = StringIO(aListOrString)
                self._headerFields = factory.allForStringIO(stringio)
                stringio.close()
