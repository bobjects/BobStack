try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import sys
sys.path.append("../../..")
# from bobstack.sipmessaging import SIPHeaderField
# from bobstack.sipmessaging import classproperty
from sipmessaging import SIPHeaderField
from sipmessaging import classproperty


class EventSIPHeaderField(SIPHeaderField):
    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_field_name(cls):
        return 'Event'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonical_compact_field_name(cls):
        return 'o'

    @classmethod
    def new_for_attributes(cls, field_name="Event", field_value_string=""):
        return cls.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)

    @property
    def is_event(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameter_named('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, a_string):
        self.parameter_named_put('adaptive-min-rate', a_string)

    @property
    def body(self):
        return self.parameter_named('body')

    @body.setter
    def body(self, a_string):
        self.parameter_named_put('body', a_string)

    @property
    def call_id(self):
        return self.parameter_named('call-id')

    @call_id.setter
    def call_id(self, a_string):
        self.parameter_named_put('call-id', a_string)

    @property
    def effective_by(self):
        return self.parameter_named('effective-by')

    @effective_by.setter
    def effective_by(self, a_string):
        self.parameter_named_put('effective-by', a_string)

    @property
    def from_tag(self):
        return self.parameter_named('from-tag')

    @from_tag.setter
    def from_tag(self, a_string):
        self.parameter_named_put('from-tag', a_string)

    @property
    def id(self):
        return self.parameter_named('id')

    @id.setter
    def id(self, a_string):
        self.parameter_named_put('id', a_string)

    @property
    def include_session_description(self):
        return self.parameter_named('include-session-description')

    @include_session_description.setter
    def include_session_description(self, a_string):
        self.parameter_named_put('include-session-description', a_string)

    @property
    def max_rate(self):
        return self.parameter_named('max-rate')

    @max_rate.setter
    def max_rate(self, a_string):
        self.parameter_named_put('max-rate', a_string)

    @property
    def min_rate(self):
        return self.parameter_named('min-rate')

    @min_rate.setter
    def min_rate(self, a_string):
        self.parameter_named_put('min-rate', a_string)

    @property
    def model(self):
        return self.parameter_named('model')

    @model.setter
    def model(self, a_string):
        self.parameter_named_put('model', a_string)

    @property
    def profile_type(self):
        return self.parameter_named('profile-type')

    @profile_type.setter
    def profile_type(self, a_string):
        self.parameter_named_put('profile-type', a_string)

    @property
    def shared(self):
        return self.parameter_named('shared')

    @shared.setter
    def shared(self, a_string):
        self.parameter_named_put('shared', a_string)

    @property
    def to_tag(self):
        return self.parameter_named('to-tag')

    @to_tag.setter
    def to_tag(self, a_string):
        self.parameter_named_put('to-tag', a_string)

    @property
    def vendor(self):
        return self.parameter_named('vendor')

    @vendor.setter
    def vendor(self, a_string):
        self.parameter_named_put('vendor', a_string)

    @property
    def version(self):
        return self.parameter_named('version')

    @version.setter
    def version(self, a_string):
        self.parameter_named_put('version', a_string)
