import inspect
from abstractSIPRequestTestCase import AbstractSIPRequestTestCase
from ..sipmessaging import SIPMessageFactory


class AbstractSIPRequestFromFactoryTestCase(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMessageClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def run_test_parsing(self):
        for message_string in self.canonicalStrings:
            request = SIPMessageFactory().next_for_string(message_string)
            self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_header_fields(self):
        raise NotImplementedError('It does not make sense to test rendering while testing factory-instantiated objects, which are parsed by definition. ' + inspect.stack()[0][3])

    def run_test_rendering_from_one_big_header_string(self):
        raise NotImplementedError('It does not make sense to test rendering while testing factory-instantiated objects, which are parsed by definition. ' + inspect.stack()[0][3])

    def run_test_rendering_from_list_of_header_field_strings(self):
        raise NotImplementedError('It does not make sense to test rendering while testing factory-instantiated objects, which are parsed by definition. ' + inspect.stack()[0][3])

    def run_test_rendering_from_list_of_field_names_and_values(self):
        raise NotImplementedError('It does not make sense to test rendering while testing factory-instantiated objects, which are parsed by definition. ' + inspect.stack()[0][3])

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        raise NotImplementedError('It does not make sense to test rendering while testing factory-instantiated objects, which are parsed by definition. ' + inspect.stack()[0][3])
