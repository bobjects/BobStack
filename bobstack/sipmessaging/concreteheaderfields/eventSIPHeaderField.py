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
    def canonicalFieldName(cls):
        return 'Event'

    # noinspection PyNestedDecorators
    @classproperty
    @classmethod
    def canonicalCompactFieldName(cls):
        return 'o'

    @classmethod
    def newForAttributes(cls, field_name="Event", field_value_string=""):
        return cls.newForFieldNameAndValueString(field_name=field_name, field_value_string=field_value_string)

    @property
    def isEvent(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameterNamed('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, a_string):
        self.parameterNamedPut('adaptive-min-rate', a_string)

    @property
    def body(self):
        return self.parameterNamed('body')

    @body.setter
    def body(self, a_string):
        self.parameterNamedPut('body', a_string)

    @property
    def call_id(self):
        return self.parameterNamed('call-id')

    @call_id.setter
    def call_id(self, a_string):
        self.parameterNamedPut('call-id', a_string)

    @property
    def effective_by(self):
        return self.parameterNamed('effective-by')

    @effective_by.setter
    def effective_by(self, a_string):
        self.parameterNamedPut('effective-by', a_string)

    @property
    def from_tag(self):
        return self.parameterNamed('from-tag')

    @from_tag.setter
    def from_tag(self, a_string):
        self.parameterNamedPut('from-tag', a_string)

    @property
    def id(self):
        return self.parameterNamed('id')

    @id.setter
    def id(self, a_string):
        self.parameterNamedPut('id', a_string)

    @property
    def include_session_description(self):
        return self.parameterNamed('include-session-description')

    @include_session_description.setter
    def include_session_description(self, a_string):
        self.parameterNamedPut('include-session-description', a_string)

    @property
    def max_rate(self):
        return self.parameterNamed('max-rate')

    @max_rate.setter
    def max_rate(self, a_string):
        self.parameterNamedPut('max-rate', a_string)

    @property
    def min_rate(self):
        return self.parameterNamed('min-rate')

    @min_rate.setter
    def min_rate(self, a_string):
        self.parameterNamedPut('min-rate', a_string)

    @property
    def model(self):
        return self.parameterNamed('model')

    @model.setter
    def model(self, a_string):
        self.parameterNamedPut('model', a_string)

    @property
    def profile_type(self):
        return self.parameterNamed('profile-type')

    @profile_type.setter
    def profile_type(self, a_string):
        self.parameterNamedPut('profile-type', a_string)

    @property
    def shared(self):
        return self.parameterNamed('shared')

    @shared.setter
    def shared(self, a_string):
        self.parameterNamedPut('shared', a_string)

    @property
    def to_tag(self):
        return self.parameterNamed('to-tag')

    @to_tag.setter
    def to_tag(self, a_string):
        self.parameterNamedPut('to-tag', a_string)

    @property
    def vendor(self):
        return self.parameterNamed('vendor')

    @vendor.setter
    def vendor(self, a_string):
        self.parameterNamedPut('vendor', a_string)

    @property
    def version(self):
        return self.parameterNamed('version')

    @version.setter
    def version(self, a_string):
        self.parameterNamedPut('version', a_string)
