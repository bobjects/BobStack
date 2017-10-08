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
        self._cache = None
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
        return self.from_cache('content_length_header_field', _content_length_header_field)

    @property
    def call_id(self):
        def _call_id():
            if self.call_id_header_field is not None:
                return self.call_id_header_field.field_value_string
            return None
        return self.from_cache('call_id', _call_id)

    @property
    def call_id_header_field(self):
        def _call_id_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_call_id), None)
        return self.from_cache('call_id_header_field', _call_id_header_field)

    @property
    def cseq(self):
        def _cseq():
            if self.cseq_header_field is not None:
                return self.cseq_header_field.field_value_string
            return None
        return self.from_cache('cseq', _cseq)

    @property
    def cseq_header_field(self):
        def _cseq_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_cseq), None)
        return self.from_cache('cseq_header_field', _cseq_header_field)

    # TODO - cache and test
    # @property
    # def to(self):
    #     if self.to_header_field is not None:
    #         return self.to_header_field.field_value_string
    #     return None

    # TODO - test
    @property
    def to_header_field(self):
        def _to_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_to), None)
        return self.from_cache('to_header_field', _to_header_field)

    # TODO - cache
    # @property
    # def from(self):
    #     if self.from_header_field is not None:
    #         return self.from_header_field.field_value_string
    #     return None

    @property
    def from_header_field(self):
        def _from_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_from), None)
        return self.from_cache('from_header_field', _from_header_field)

    @property
    def max_forwards(self):
        def _max_forwards():
            if self.max_forwards_header_field is not None:
                return self.max_forwards_header_field.integer_value
            return None
        return self.from_cache('max_forwards', _max_forwards)

    @property
    def max_forwards_header_field(self):
        def _max_forwards_header_field():
            return next((header_field for header_field in self.header_fields if header_field.is_max_forwards), None)
        return self.from_cache('max_forwards_header_field', _max_forwards_header_field)

    @property
    def vias(self):
        def _vias():
            return [x.field_value_string for x in self.via_header_fields]
        return self.from_cache('vias', _vias)

    @property
    def via_header_fields(self):
        def _via_header_fields():
            return [header_field for header_field in self.header_fields if header_field.is_via]
        return self.from_cache('via_header_fields', _via_header_fields)

    @property
    def route_header_fields(self):
        def _route_header_fields():
            return [header_field for header_field in self.header_fields if header_field.is_route]
        return self.from_cache('route_header_fields', _route_header_fields)

    @property
    def route_uris(self):
        def _route_uris():
            return [x.sip_uri for x in self.route_header_fields]
        return self.from_cache('route_uris', _route_uris)

    @property
    def record_route_header_fields(self):
        def _record_route_header_fields():
            return [header_field for header_field in self.header_fields if header_field.is_record_route]
        return self.from_cache('record_route_header_fields', _record_route_header_fields)

    @property
    def record_route_uris(self):
        def _record_route_uris():
            return [x.sip_uri for x in self.record_route_header_fields]
        return self.from_cache('record_route_uris', _record_route_uris)

    # TODO:  need to test
    def add_header_field(self, a_sip_header_field):
        if a_sip_header_field:
            self.header_fields.append(a_sip_header_field)
            self.initialize_cache()

    # TODO:  need to test
    def add_header_fields(self, a_list_of_sip_header_field):
        for hf in a_list_of_sip_header_field:
            self.add_header_field(hf)

    # TODO:  need to test (partially tested)
    def add_header_field_after_header_fields_of_same_class(self, a_header_field):
        header_fields = self.header_fields
        class_index = -1
        to_from_index = -1
        for i, header in enumerate(header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if header.__class__.__name__ == a_header_field.__class__.__name__:
                class_index = i
            if header.is_to:
                to_from_index = i
            if header.is_from:
                to_from_index = i
        insertion_index = class_index
        if insertion_index == -1:
            insertion_index = to_from_index
        header_fields.insert(insertion_index + 1, a_header_field)
        self.header_fields = header_fields

    # TODO:  need to test (partially tested)
    def add_header_field_before_header_fields_of_same_class(self, a_header_field):
        header_fields = self.header_fields
        class_index = -1
        to_from_index = -1
        for i, header in enumerate(header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if header.__class__.__name__ == a_header_field.__class__.__name__:
                if class_index == -1:
                    class_index = i
            if header.is_to:
                to_from_index = i
            if header.is_from:
                to_from_index = i
        insertion_index = class_index
        if insertion_index == -1:
            insertion_index = to_from_index + 1
        header_fields.insert(max(0, insertion_index), a_header_field)
        self.header_fields = header_fields

    # TODO: need to test (partially tested)
    def remove_first_header_field_of_class(self, a_class):
        for i, j in enumerate(self.header_fields):
            # TODO: Really sorry, but when we pass the class in from a different module,
            # the class is different.  Trap for young players.  We need to do better than this class name comparison.
            if j.__class__.__name__ is a_class.__name__:
                self.header_fields.pop(i)
                self.initialize_cache()
                return

    @property
    def known_header_fields(self):
        def _known_header_fields():
            return [header_field for header_field in self.header_fields if header_field.is_known]
        return self.from_cache('known_header_fields', _known_header_fields)

    @property
    def unknown_header_fields(self):
        def _unknown_header_fields():
            return [header_field for header_field in self.header_fields if header_field.is_unknown]
        return self.from_cache('unknown_header_fields', _unknown_header_fields)

    @property
    def is_valid(self):
        def _is_valid():
            return all(f.is_valid for f in self.header_fields)
        return self.from_cache('is_valid', _is_valid)

    # TODO:  it would also be nice to make this object iterable and indexable.  E.g. someHeader[3] to get someHeader.header_fields[3]
    @property
    def header_fields(self):
        return self._headerFields

    @header_fields.setter
    def header_fields(self, a_list_or_string):
        self.initialize_cache()
        if not a_list_or_string:
            self._headerFields = []
        else:
            factory = SIPHeaderFieldFactory()
            if isinstance(a_list_or_string, list):
                if isinstance(a_list_or_string[0], basestring):  # list of complete header field strings
                    self._headerFields = [factory.next_for_string(s) for s in a_list_or_string]
                elif isinstance(a_list_or_string[0], (list, tuple)):  # list of field names and field values
                    header_fields = []
                    for field_name, field_value_string in a_list_or_string:
                        if isinstance(field_value_string, dict):  # field_value_string is dict of property names and values.
                            header_field = factory.next_for_field_name(field_name)
                            for propertyName, propertyValue in field_value_string.iteritems():
                                prop = next(c.__dict__.get(propertyName, None) for c in header_field.__class__.__mro__ if propertyName in c.__dict__)
                                if type(prop) is property:
                                    setter = prop.fset
                                    if setter:
                                        setter(header_field, propertyValue)
                            header_fields.append(header_field)
                        else:
                            header_fields.append(factory.next_for_field_name_and_field_value(field_name, str(field_value_string)))
                    self._headerFields = header_fields
                else:
                    self._headerFields = a_list_or_string  # list of SIPHeaderField instances
            else:  # One big multiline string
                stringio = StringIO(a_list_or_string)
                self._headerFields = factory.all_for_stringio(stringio)
                stringio.close()

    @property
    def transaction_hash(self):
        # cseq + branch id on Via header (the last one, which is the via of the original request)
        def _transaction_hash():
            answer = None
            via_fields = self.via_header_fields
            cseq = self.cseq
            if via_fields:
                original_via_field = via_fields[-1]
                if original_via_field.branch and cseq:
                    answer = sha1()
                    answer.update(original_via_field.branch)
                    answer.update(cseq)
                    answer = answer.hexdigest()
            return answer
        return self.from_cache('transaction_hash', _transaction_hash)

    @property
    def dialog_hash(self):
        def _dialog_hash():
            answer = None
            to_tag = self.to_tag
            from_tag = self.from_tag
            call_id = self.call_id
            if to_tag and from_tag and call_id:
                answer = sha1()
                answer.update(to_tag)
                answer.update(from_tag)
                answer.update(call_id)
                answer = answer.hexdigest()
            return answer
        return self.from_cache('dialog_hash', _dialog_hash)

    @property
    def invariant_branch_hash(self):
        # TODO: we may need to extend this when we want to be resilient to loop and spiral detection
        # See section 16.6 point 8 of RFC3261.
        def _invariant_branch_hash():
            answer = sha1()
            # It's OK if some of these are None.
            answer.update(str(self.to_tag))
            answer.update(str(self.from_tag))
            answer.update(str(self.call_id))
            answer.update(str(self.cseq))
            if self.vias:
                answer.update(self.vias[0])
            return answer.hexdigest()
        return self.from_cache('invariant_branch_hash', _invariant_branch_hash)

    @property
    def to_tag(self):
        def _to_tag():
            to_header_field = self.to_header_field
            if to_header_field:
                return to_header_field.tag
            return None
        return self.from_cache('to_tag', _to_tag)

    @property
    def from_tag(self):
        def _from_tag():
            from_header_field = self.from_header_field
            if from_header_field:
                return from_header_field.tag
            return None
        return self.from_cache('from_tag', _from_tag)

    def from_cache(self, key, value_function):
        try:
            return self._cache[key]
        except KeyError:
            answer = value_function()
            self._cache[key] = answer
            return answer
