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
    def newForAttributes(cls, fieldName="Event", fieldValueString=""):
        return cls.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)

    @property
    def isEvent(self):
        return True

    # http://www.iana.org/assignments/sip-parameters/sip-parameters.xhtml#sip-parameters-2
    @property
    def adaptive_min_rate(self):
        return self.parameterNamed('adaptive-min-rate')

    @adaptive_min_rate.setter
    def adaptive_min_rate(self, aString):
        self.parameterNamedPut('adaptive-min-rate', aString)

    @property
    def body(self):
        return self.parameterNamed('body')

    @body.setter
    def body(self, aString):
        self.parameterNamedPut('body', aString)

    @property
    def call_id(self):
        return self.parameterNamed('call-id')

    @call_id.setter
    def call_id(self, aString):
        self.parameterNamedPut('call-id', aString)

    @property
    def effective_by(self):
        return self.parameterNamed('effective-by')

    @effective_by.setter
    def effective_by(self, aString):
        self.parameterNamedPut('effective-by', aString)

    @property
    def from_tag(self):
        return self.parameterNamed('from-tag')

    @from_tag.setter
    def from_tag(self, aString):
        self.parameterNamedPut('from-tag', aString)

    @property
    def id(self):
        return self.parameterNamed('id')

    @id.setter
    def id(self, aString):
        self.parameterNamedPut('id', aString)

    @property
    def include_session_description(self):
        return self.parameterNamed('include-session-description')

    @include_session_description.setter
    def include_session_description(self, aString):
        self.parameterNamedPut('include-session-description', aString)

    @property
    def max_rate(self):
        return self.parameterNamed('max-rate')

    @max_rate.setter
    def max_rate(self, aString):
        self.parameterNamedPut('max-rate', aString)

    @property
    def min_rate(self):
        return self.parameterNamed('min-rate')

    @min_rate.setter
    def min_rate(self, aString):
        self.parameterNamedPut('min-rate', aString)

    @property
    def model(self):
        return self.parameterNamed('model')

    @model.setter
    def model(self, aString):
        self.parameterNamedPut('model', aString)

    @property
    def profile_type(self):
        return self.parameterNamed('profile-type')

    @profile_type.setter
    def profile_type(self, aString):
        self.parameterNamedPut('profile-type', aString)

    @property
    def shared(self):
        return self.parameterNamed('shared')

    @shared.setter
    def shared(self, aString):
        self.parameterNamedPut('shared', aString)

    @property
    def to_tag(self):
        return self.parameterNamed('to-tag')

    @to_tag.setter
    def to_tag(self, aString):
        self.parameterNamedPut('to-tag', aString)

    @property
    def vendor(self):
        return self.parameterNamed('vendor')

    @vendor.setter
    def vendor(self, aString):
        self.parameterNamedPut('vendor', aString)

    @property
    def version(self):
        return self.parameterNamed('version')

    @version.setter
    def version(self, aString):
        self.parameterNamedPut('version', aString)
