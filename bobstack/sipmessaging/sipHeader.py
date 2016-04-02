try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from hashlib import sha1
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
        self._viaHeaderFields = None
        self._transactionHash = None
        self._dialogHash = None
        # TODO: need to add other header field attributes besides just content-length and via.

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
            return self.contentLengthHeaderField.integerValue
        return 0

    @property
    def contentLengthHeaderField(self):
        if self._contentLengthHeaderField is None:
            self._contentLengthHeaderField = next((headerField for headerField in self.headerFields if headerField.isContentLength), None)
        return self._contentLengthHeaderField

    # TODO - cache and test
    @property
    def callID(self):
        if self.callIDHeaderField is not None:
            return self.callIDHeaderField.fieldValueString
        return None

    # TODO - cache and test
    @property
    def callIDHeaderField(self):
        return next((headerField for headerField in self.headerFields if headerField.isCallID), None)

    # TODO - cache and test
    @property
    def cSeq(self):
        if self.cSeqHeaderField is not None:
            return self.cSeqHeaderField.fieldValueString
        return None

    # TODO - cache and test
    @property
    def cSeqHeaderField(self):
        return next((headerField for headerField in self.headerFields if headerField.isCSeq), None)

    # TODO - cache and test
    # @property
    # def to(self):
    #     if self.toHeaderField is not None:
    #         return self.toHeaderField.fieldValueString
    #     return None

    # TODO - cache and test
    @property
    def toHeaderField(self):
        return next((headerField for headerField in self.headerFields if headerField.isTo), None)

    # TODO - cache and test
    # @property
    # def from(self):
    #     if self.fromHeaderField is not None:
    #         return self.fromHeaderField.fieldValueString
    #     return None

    # TODO - cache and test
    @property
    def fromHeaderField(self):
        return next((headerField for headerField in self.headerFields if headerField.isFrom), None)

    @property
    def vias(self):
        if self._viaHeaderFields is not None:
            return [x.fieldValueString for x in self._viaHeaderFields]
        return []

    @property
    def viaHeaderFields(self):
        if self._viaHeaderFields is None:
            self._viaHeaderFields = [headerField for headerField in self.headerFields if headerField.isVia]
        return self._viaHeaderFields

    # TODO:  need to test
    def addHeaderFieldAfterHeaderFieldsOfSameClass(self, aHeaderField):
        headerFields = self.headerFields
        classIndex = -1
        toFromIndex = -1
        for i, header in enumerate(headerFields):
            if header.__class__ == aHeaderField.__class__:
                classIndex = i
            if header.isTo:
                toFromIndex = i
            if header.isFrom:
                toFromIndex = i
        insertionIndex = classIndex
        if insertionIndex == -1:
            insertionIndex = toFromIndex
        headerFields.insert(insertionIndex + 1, aHeaderField)
        self.headerFields = headerFields

    # TODO:  need to test
    def addHeaderFieldBeforeHeaderFieldsOfSameClass(self, aHeaderField):
        headerFields = self.headerFields
        classIndex = -1
        toFromIndex = -1
        for i, header in enumerate(headerFields):
            if header.__class__ == aHeaderField.__class__:
                classIndex = i
            if header.isTo:
                toFromIndex = i
            if header.isFrom:
                toFromIndex = i
        insertionIndex = classIndex
        if insertionIndex == -1:
            insertionIndex = toFromIndex
        headerFields.insert(max(0, insertionIndex), aHeaderField)
        self.headerFields = headerFields

    @property
    def knownHeaderFields(self):
        if not self._knownHeaderFields:
            self._knownHeaderFields = [headerField for headerField in self.headerFields if headerField.isKnown]
        return self._knownHeaderFields

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
                    for fieldName, fieldValueString in aListOrString:
                        if isinstance(fieldValueString, dict):  # fieldValueString is dict of property names and values.
                            headerField = factory.nextForFieldName(fieldName)
                            for propertyName, propertyValue in fieldValueString.iteritems():
                                prop = next(c.__dict__.get(propertyName, None) for c in headerField.__class__.__mro__ if propertyName in c.__dict__)
                                if type(prop) is property:
                                    setter = prop.fset
                                    if setter:
                                        setter(headerField, propertyValue)
                            headerFields.append(headerField)
                        else:
                            headerFields.append(factory.nextForFieldNameAndFieldValue(fieldName, str(fieldValueString)))
                    self._headerFields = headerFields
                else:
                    self._headerFields = aListOrString  # list of SIPHeaderField instances
            else:  # One big multiline string
                stringio = StringIO(aListOrString)
                self._headerFields = factory.allForStringIO(stringio)
                stringio.close()

    # TODO: implement properties used here.
    # TODO:  need to test.
    @property
    def transactionHash(self):
        # cseq + branch id on Via header (the last one, which is the via of the original request)
        if not self._transactionHash:
            viaFields = self.viaHeaderFields
            cseq = self.cSeq
            if viaFields:
                originalViaField = viaFields[-1]
                if originalViaField.branch and cseq:
                    answer = sha1()
                    answer.update(originalViaField.branch)
                    answer.update(cseq)
                    self._transactionHash = answer.hexdigest()
        return self._transactionHash

    # TODO:  need to test.
    @property
    def dialogHash(self):
        if not self._dialogHash:
            toTag = self.toTag
            fromTag = self.fromTag
            callID = self.callID
            if toTag and fromTag and callID:
                answer = sha1()
                answer.update(toTag)
                answer.update(fromTag)
                answer.update(callID)
                self._dialogHash = answer.hexdigest()
        return self._dialogHash

    # TODO:  need to test.
    @property
    def toTag(self):
        toHeaderField = self.toHeaderField
        if toHeaderField:
            return toHeaderField.tag

    # TODO
    @property
    def fromTag(self):
        fromHeaderField = self.fromHeaderField
        if fromHeaderField:
            return fromHeaderField.tag

