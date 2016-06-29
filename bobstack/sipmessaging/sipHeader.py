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
        self.initializeCache()

    def initializeCache(self):
        self._headerFields = []
        self._knownHeaderFields = None
        self._unknownHeaderFields = None
        self._contentLengthHeaderField = None
        self._toHeaderField = None
        self._fromHeaderField = None
        self._viaHeaderFields = None
        self._routeHeaderFields = None
        self._recordRouteHeaderFields = None
        self._maxForwardsHeaderField = None
        self._cSeqHeaderField = None
        self._callIDHeaderField = None
        self._transactionHash = None
        self._dialogHash = None

        self._invariantBranchHash = None
        self._toTag = None
        self._fromTag = None

    def parseAttributesFromStringIO(self, stringioToParse):
        # TODO: don't forget to test folding in this factory method.  That's separate from the other technique.
        self.initializeCache()
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

    # TODO - cache
    @property
    def callID(self):
        if self.callIDHeaderField is not None:
            return self.callIDHeaderField.fieldValueString
        return None

    @property
    def callIDHeaderField(self):
        if self._callIDHeaderField is None:
            self._callIDHeaderField = next((headerField for headerField in self.headerFields if headerField.isCallID), None)
        return self._callIDHeaderField

    # TODO - cache
    @property
    def cSeq(self):
        if self.cSeqHeaderField is not None:
            return self.cSeqHeaderField.fieldValueString
        return None

    @property
    def cSeqHeaderField(self):
        if self._cSeqHeaderField is None:
            self._cSeqHeaderField = next((headerField for headerField in self.headerFields if headerField.isCSeq), None)
        return self._cSeqHeaderField

    # TODO - cache and test
    # @property
    # def to(self):
    #     if self.toHeaderField is not None:
    #         return self.toHeaderField.fieldValueString
    #     return None

    # TODO - test
    @property
    def toHeaderField(self):
        if self._toHeaderField is None:
            self._toHeaderField = next((headerField for headerField in self.headerFields if headerField.isTo), None)
        return self._toHeaderField

    # TODO - cache
    # @property
    # def from(self):
    #     if self.fromHeaderField is not None:
    #         return self.fromHeaderField.fieldValueString
    #     return None

    @property
    def fromHeaderField(self):
        if self._fromHeaderField is None:
            self._fromHeaderField = next((headerField for headerField in self.headerFields if headerField.isFrom), None)
        return self._fromHeaderField

    # TODO - cache
    @property
    def maxForwards(self):
         if self.maxForwardsHeaderField is not None:
             return self.maxForwardsHeaderField.integerValue
         return None

    @property
    def maxForwardsHeaderField(self):
        if self._maxForwardsHeaderField is None:
            self._maxForwardsHeaderField = next((headerField for headerField in self.headerFields if headerField.isMaxForwards), None)
        return self._maxForwardsHeaderField

    # TODO - cache
    @property
    def vias(self):
        return [x.fieldValueString for x in self.viaHeaderFields]

    @property
    def viaHeaderFields(self):
        if self._viaHeaderFields is None:
            self._viaHeaderFields = [headerField for headerField in self.headerFields if headerField.isVia]
        return self._viaHeaderFields

    @property
    def routeHeaderFields(self):
        if self._routeHeaderFields is None:
            self._routeHeaderFields = [headerField for headerField in self.headerFields if headerField.isRoute]
        return self._routeHeaderFields

    # TODO - cache
    @property
    def routeURIs(self):
        return [x.sipURI for x in self.routeHeaderFields]

    @property
    def recordRouteHeaderFields(self):
        if self._recordRouteHeaderFields is None:
            self._recordRouteHeaderFields = [headerField for headerField in self.headerFields if headerField.isRecordRoute]
        return self._recordRouteHeaderFields

    # TODO - cache
    @property
    def recordRouteURIs(self):
        return [x.sipURI for x in self.recordRouteHeaderFields]

    # TODO:  need to test
    def addHeaderField(self, aSIPHeaderField):
        self.headerFields.append(aSIPHeaderField)

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

    # TODO: need to test
    def removeFirstHeaderFieldOfClass(self, aClass):
        for i, j in enumerate(self.headerFields):
            if j.__class__ is aClass:
                self.headerFields.pop(i)
                return

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

    # TODO: cache
    @property
    def isValid(self):
        return all(f.isValid for f in self.headerFields)

    # TODO:  it would also be nice to make this object iterable and indexable.  E.g. someHeader[3] to get someHeader.headerFields[3]
    @property
    def headerFields(self):
        return self._headerFields

    @headerFields.setter
    def headerFields(self, aListOrString):
        self.initializeCache()
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

    @property
    def invariantBranchHash(self):
        if self._invariantBranchHash is None:
            # TODO: we may need to extend this when we want to be resilient to loop and spiral detection
            # See section 16.6 point 8 of RFC3261.
            answer = sha1()
            # It's OK if some of these are None.
            answer.update(str(self.toTag))
            answer.update(str(self.fromTag))
            answer.update(str(self.callID))
            answer.update(str(self.cSeq))
            if self.vias:
                answer.update(self.vias[0])
            self._invariantBranchHash = answer.hexdigest()
        return self._invariantBranchHash

    @property
    def toTag(self):
        if self._toTag is None:
            toHeaderField = self.toHeaderField
            if toHeaderField:
                self._toTag = toHeaderField.tag
        return self._toTag

    @property
    def fromTag(self):
        if self._fromTag is None:
            fromHeaderField = self.fromHeaderField
            if fromHeaderField:
                self._fromTag = fromHeaderField.tag
        return self._fromTag
