try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from hashlib import sha1
from sipHeaderFieldFactory import SIPHeaderFieldFactory


class SIPHeader(object):
    @classmethod
    def new_parsed_from(cls, stringio_to_parse):
        answer = cls()
        answer.parse_attributes_from_stringio(stringio_to_parse)
        return answer

    @classmethod
    def new_for_attributes(cls, header_fields=None):
        answer = cls()
        if not header_fields:
            answer.header_fields = []
        else:
            answer.header_fields = header_fields
        return answer

    def __init__(self):
        self._headerFields = []
        self.initialize_cache()

    def initialize_cache(self):
        self._cache = {}

    def parse_attributes_from_stringio(self, stringio_to_parse):
        # TODO: don't forget to test folding in this factory method.  That's separate from the other technique.
        self.initialize_cache()
        self._headerFields = SIPHeaderFieldFactory().all_for_stringio(stringio_to_parse)

    def render_raw_string_from_attributes(self, stringio):
        for header_field in self.header_fields:
            stringio.write(header_field.raw_string)
            stringio.write("\r\n")
        stringio.write("\r\n")

    # TODO: cache
    @property
    def content_length(self):
        if self.content_length_header_field is not None:
            return self.content_length_header_field.integer_value
        return 0

    @property
    def content_length_header_field(self):
        def _content_length_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_content_length), None)
        return self.fromCache('content_length_header_field', _content_length_header_field)

    @property
    def callID(self):
        def _callID():
            if self.callIDHeaderField is not None:
                return self.callIDHeaderField.field_value_string
            return None
        return self.fromCache('callID', _callID)

    @property
    def callIDHeaderField(self):
        def _callIDHeaderField():
            return next((header_field for header_field in self.header_fields if header_field.is_call_id), None)
        return self.fromCache('callIDHeaderField', _callIDHeaderField)

    @property
    def cSeq(self):
        def _cSeq():
            if self.cSeqHeaderField is not None:
                return self.cSeqHeaderField.field_value_string
            return None
        return self.fromCache('cSeq', _cSeq)

    @property
    def cSeqHeaderField(self):
        def _cSeqHeaderField():
            return next((header_field for header_field in self.header_fields if header_field.is_cseq), None)
        return self.fromCache('cSeqHeaderField', _cSeqHeaderField)

    # TODO - cache and test
    # @property
    # def to(self):
    #     if self.toHeaderField is not None:
    #         return self.toHeaderField.field_value_string
    #     return None

    # TODO - test
    @property
    def toHeaderField(self):
        def _toHeaderField():
            return next((header_field for header_field in self.header_fields if header_field.is_to), None)
        return self.fromCache('toHeaderField', _toHeaderField)

    # TODO - cache
    # @property
    # def from(self):
    #     if self.fromHeaderField is not None:
    #         return self.fromHeaderField.field_value_string
    #     return None

    @property
    def fromHeaderField(self):
        def _fromHeaderField():
            return next((header_field for header_field in self.header_fields if header_field.is_from), None)
        return self.fromCache('fromHeaderField', _fromHeaderField)

    @property
    def max_forwards(self):
        def _maxForwards():
            if self.maxForwardsHeaderField is not None:
                return self.maxForwardsHeaderField.integer_value
            return None
        return self.fromCache('max_forwards', _maxForwards)

    @property
    def maxForwardsHeaderField(self):
        def _maxForwardsHeaderField():
            return next((header_field for header_field in self.header_fields if header_field.is_max_forwards), None)
        return self.fromCache('maxForwardsHeaderField', _maxForwardsHeaderField)

    @property
    def vias(self):
        def _vias():
            return [x.field_value_string for x in self.viaHeaderFields]
        return self.fromCache('vias', _vias)

    @property
    def viaHeaderFields(self):
        def _viaHeaderFields():
            return [header_field for header_field in self.header_fields if header_field.is_via]
        return self.fromCache('viaHeaderFields', _viaHeaderFields)

    @property
    def routeHeaderFields(self):
        def _routeHeaderFields():
            return [header_field for header_field in self.header_fields if header_field.is_route]
        return self.fromCache('routeHeaderFields', _routeHeaderFields)

    @property
    def routeURIs(self):
        def _routeURIs():
            return [x.sip_uri for x in self.routeHeaderFields]
        return self.fromCache('routeURIs', _routeURIs)

    @property
    def recordRouteHeaderFields(self):
        def _recordRouteHeaderFields():
            return [header_field for header_field in self.header_fields if header_field.is_record_route]
        return self.fromCache('recordRouteHeaderFields', _recordRouteHeaderFields)

    @property
    def recordRouteURIs(self):
        def _recordRouteURIs():
            return [x.sip_uri for x in self.recordRouteHeaderFields]
        return self.fromCache('recordRouteURIs', _recordRouteURIs)

    # TODO:  need to test
    def add_header_field(self, a_sip_header_field):
        if a_sip_header_field:
            self.header_fields.append(a_sip_header_field)
            self.initialize_cache()

    # TODO:  need to test
    def addHeaderFields(self, a_list_of_sip_header_field):
        for hf in a_list_of_sip_header_field:
            self.add_header_field(hf)

    # TODO:  need to test (partially tested)
    def addHeaderFieldAfterHeaderFieldsOfSameClass(self, a_header_field):
        header_fields = self.header_fields
        class_index = -1
        toFromIndex = -1
        for i, header in enumerate(header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if header.__class__.__name__ == a_header_field.__class__.__name__:
                class_index = i
            if header.is_to:
                toFromIndex = i
            if header.is_from:
                toFromIndex = i
        insertionIndex = class_index
        if insertionIndex == -1:
            insertionIndex = toFromIndex
        header_fields.insert(insertionIndex + 1, a_header_field)
        self.header_fields = header_fields

    # TODO:  need to test (partially tested)
    def addHeaderFieldBeforeHeaderFieldsOfSameClass(self, a_header_field):
        header_fields = self.header_fields
        class_index = -1
        toFromIndex = -1
        for i, header in enumerate(header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if header.__class__.__name__ == a_header_field.__class__.__name__:
                if class_index == -1:
                    class_index = i
            if header.is_to:
                toFromIndex = i
            if header.is_from:
                toFromIndex = i
        insertionIndex = class_index
        if insertionIndex == -1:
            insertionIndex = toFromIndex + 1
        header_fields.insert(max(0, insertionIndex), a_header_field)
        self.header_fields = header_fields

    # TODO: need to test (partially tested)
    def removeFirstHeaderFieldOfClass(self, aClass):
        for i, j in enumerate(self.header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if j.__class__.__name__ is aClass.__name__:
                self.header_fields.pop(i)
                self.initialize_cache()
                return

    @property
    def knownHeaderFields(self):
        def _knownHeaderFields():
            return [header_field for header_field in self.header_fields if header_field.is_known]
        return self.fromCache('knownHeaderFields', _knownHeaderFields)

    @property
    def unknownHeaderFields(self):
        def _unknownHeaderFields():
            return [header_field for header_field in self.header_fields if header_field.isUnknown]
        return self.fromCache('unknownHeaderFields', _unknownHeaderFields)

    @property
    def is_valid(self):
        def _isValid():
            return all(f.is_valid for f in self.header_fields)
        return self.fromCache('is_valid', _isValid)

    # TODO:  it would also be nice to make this object iterable and indexable.  E.g. someHeader[3] to get someHeader.header_fields[3]
    @property
    def header_fields(self):
        return self._headerFields

    @header_fields.setter
    def header_fields(self, aListOrString):
        self.initialize_cache()
        if not aListOrString:
            self._headerFields = []
        else:
            factory = SIPHeaderFieldFactory()
            if isinstance(aListOrString, list):
                if isinstance(aListOrString[0], basestring):  # list of complete header field strings
                    self._headerFields = [factory.next_for_string(s) for s in aListOrString]
                elif isinstance(aListOrString[0], (list, tuple)):  # list of field names and field values
                    header_fields = []
                    for field_name, field_value_string in aListOrString:
                        if isinstance(field_value_string, dict):  # field_value_string is dict of property names and values.
                            header_field = factory.nextForFieldName(field_name)
                            for propertyName, propertyValue in field_value_string.iteritems():
                                prop = next(c.__dict__.get(propertyName, None) for c in header_field.__class__.__mro__ if propertyName in c.__dict__)
                                if type(prop) is property:
                                    setter = prop.fset
                                    if setter:
                                        setter(header_field, propertyValue)
                            header_fields.append(header_field)
                        else:
                            header_fields.append(factory.nextForFieldNameAndFieldValue(field_name, str(field_value_string)))
                    self._headerFields = header_fields
                else:
                    self._headerFields = aListOrString  # list of SIPHeaderField instances
            else:  # One big multiline string
                stringio = StringIO(aListOrString)
                self._headerFields = factory.all_for_stringio(stringio)
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
