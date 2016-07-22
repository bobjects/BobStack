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
        self.initializeCache()

    def initializeCache(self):
        self._cache = {}

    def parseAttributesFromStringIO(self, stringioToParse):
        # TODO: don't forget to test folding in this factory method.  That's separate from the other technique.
        self.initializeCache()
        self._headerFields = SIPHeaderFieldFactory().allForStringIO(stringioToParse)

    def renderRawStringFromAttributes(self, stringio):
        for headerField in self.headerFields:
            stringio.write(headerField.rawString)
            stringio.write("\r\n")
        stringio.write("\r\n")

    # TODO: cache
    @property
    def contentLength(self):
        if self.contentLengthHeaderField is not None:
            return self.contentLengthHeaderField.integerValue
        return 0

    @property
    def contentLengthHeaderField(self):
        def _contentLengthHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isContentLength), None)
        return self.fromCache('contentLengthHeaderField', _contentLengthHeaderField)

    @property
    def callID(self):
        def _callID():
            if self.callIDHeaderField is not None:
                return self.callIDHeaderField.fieldValueString
            return None
        return self.fromCache('callID', _callID)

    @property
    def callIDHeaderField(self):
        def _callIDHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isCallID), None)
        return self.fromCache('callIDHeaderField', _callIDHeaderField)

    @property
    def cSeq(self):
        def _cSeq():
            if self.cSeqHeaderField is not None:
                return self.cSeqHeaderField.fieldValueString
            return None
        return self.fromCache('cSeq', _cSeq)

    @property
    def cSeqHeaderField(self):
        def _cSeqHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isCSeq), None)
        return self.fromCache('cSeqHeaderField', _cSeqHeaderField)

    # TODO - cache and test
    # @property
    # def to(self):
    #     if self.toHeaderField is not None:
    #         return self.toHeaderField.fieldValueString
    #     return None

    # TODO - test
    @property
    def toHeaderField(self):
        def _toHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isTo), None)
        return self.fromCache('toHeaderField', _toHeaderField)

    # TODO - cache
    # @property
    # def from(self):
    #     if self.fromHeaderField is not None:
    #         return self.fromHeaderField.fieldValueString
    #     return None

    @property
    def fromHeaderField(self):
        def _fromHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isFrom), None)
        return self.fromCache('fromHeaderField', _fromHeaderField)

    @property
    def maxForwards(self):
        def _maxForwards():
            if self.maxForwardsHeaderField is not None:
                return self.maxForwardsHeaderField.integerValue
            return None
        return self.fromCache('maxForwards', _maxForwards)

    @property
    def maxForwardsHeaderField(self):
        def _maxForwardsHeaderField():
            return next((headerField for headerField in self.headerFields if headerField.isMaxForwards), None)
        return self.fromCache('maxForwardsHeaderField', _maxForwardsHeaderField)

    @property
    def vias(self):
        def _vias():
            return [x.fieldValueString for x in self.viaHeaderFields]
        return self.fromCache('vias', _vias)

    @property
    def viaHeaderFields(self):
        def _viaHeaderFields():
            return [headerField for headerField in self.headerFields if headerField.isVia]
        return self.fromCache('viaHeaderFields', _viaHeaderFields)

    @property
    def routeHeaderFields(self):
        def _routeHeaderFields():
            return [headerField for headerField in self.headerFields if headerField.isRoute]
        return self.fromCache('routeHeaderFields', _routeHeaderFields)

    @property
    def routeURIs(self):
        def _routeURIs():
            return [x.sipURI for x in self.routeHeaderFields]
        return self.fromCache('routeURIs', _routeURIs)

    @property
    def recordRouteHeaderFields(self):
        def _recordRouteHeaderFields():
            return [headerField for headerField in self.headerFields if headerField.isRecordRoute]
        return self.fromCache('recordRouteHeaderFields', _recordRouteHeaderFields)

    @property
    def recordRouteURIs(self):
        def _recordRouteURIs():
            return [x.sipURI for x in self.recordRouteHeaderFields]
        return self.fromCache('recordRouteURIs', _recordRouteURIs)

    # TODO:  need to test
    def addHeaderField(self, aSIPHeaderField):
        if aSIPHeaderField:
            self.headerFields.append(aSIPHeaderField)
            self.initializeCache()

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
                self.initializeCache()
                return

    @property
    def knownHeaderFields(self):
        def _knownHeaderFields():
            return [headerField for headerField in self.headerFields if headerField.isKnown]
        return self.fromCache('knownHeaderFields', _knownHeaderFields)

    @property
    def unknownHeaderFields(self):
        def _unknownHeaderFields():
            return [headerField for headerField in self.headerFields if headerField.isUnknown]
        return self.fromCache('unknownHeaderFields', _unknownHeaderFields)

    @property
    def isValid(self):
        def _isValid():
            return all(f.isValid for f in self.headerFields)
        return self.fromCache('isValid', _isValid)

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

    @property
    def transactionHash(self):
        # cseq + branch id on Via header (the last one, which is the via of the original request)
        def _transactionHash():
            answer = None
            viaFields = self.viaHeaderFields
            cseq = self.cSeq
            if viaFields:
                originalViaField = viaFields[-1]
                if originalViaField.branch and cseq:
                    answer = sha1()
                    answer.update(originalViaField.branch)
                    answer.update(cseq)
                    answer = answer.hexdigest()
            return answer
        return self.fromCache('transactionHash', _transactionHash)

    @property
    def dialogHash(self):
        def _dialogHash():
            answer = None
            toTag = self.toTag
            fromTag = self.fromTag
            callID = self.callID
            if toTag and fromTag and callID:
                answer = sha1()
                answer.update(toTag)
                answer.update(fromTag)
                answer.update(callID)
                answer = answer.hexdigest()
            return answer
        return self.fromCache('dialogHash', _dialogHash)

    @property
    def invariantBranchHash(self):
        # TODO: we may need to extend this when we want to be resilient to loop and spiral detection
        # See section 16.6 point 8 of RFC3261.
        def _invariantBranchHash():
            answer = sha1()
            # It's OK if some of these are None.
            answer.update(str(self.toTag))
            answer.update(str(self.fromTag))
            answer.update(str(self.callID))
            answer.update(str(self.cSeq))
            if self.vias:
                answer.update(self.vias[0])
            return answer.hexdigest()
        return self.fromCache('invariantBranchHash', _invariantBranchHash)

    @property
    def toTag(self):
        def _toTag():
            toHeaderField = self.toHeaderField
            if toHeaderField:
                return toHeaderField.tag
            return None
        return self.fromCache('toTag', _toTag)

    @property
    def fromTag(self):
        def _fromTag():
            fromHeaderField = self.fromHeaderField
            if fromHeaderField:
                return fromHeaderField.tag
            return None
        return self.fromCache('fromTag', _fromTag)

    def fromCache(self, key, valueFunction):
        try:
            return self._cache[key]
        except KeyError:
            answer = valueFunction()
            self._cache[key] = answer
            return answer
