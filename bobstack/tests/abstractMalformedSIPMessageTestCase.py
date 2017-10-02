import inspect
from abstractSIPMessageTestCase import AbstractSIPMessageTestCase
from sipmessaging import SIPHeader
from sipmessaging import MalformedSIPStartLine


class AbstractMalformedSIPMessageTestCase(AbstractSIPMessageTestCase):
    @property
    def sipMethodString(self):
        # For a malformed message, this is just for building the header strings.
        return "INVITE"

    @property
    def canonicalStartLineStrings(self):
        # TODO - Moar???
        return ["Malformed start line"]

    @property
    def sipMessageClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    def runAssertionsForSIPMessage(self, a_sip_message):
        super(AbstractMalformedSIPMessageTestCase, self).runAssertionsForSIPMessage(a_sip_message)
        self.assertFalse(a_sip_message.is_valid)
        self.assertFalse(a_sip_message.is_request)
        self.assertFalse(a_sip_message.is_response)
        self.assertTrue(a_sip_message.is_malformed)
        self.assertFalse(a_sip_message.start_line.is_request)
        self.assertFalse(a_sip_message.start_line.is_response)
        self.assertTrue(a_sip_message.start_line.is_malformed)
        self.assertEqual(self.canonicalStartLineStrings[0], a_sip_message.start_line.raw_string)

    def run_test_parsing(self):
        for message_string in self.canonicalStrings:
            message = self.sipMessageClassUnderTest.new_parsed_from(message_string)
            self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_header_fields(self):
        header_fields = self.listOfHeaderFieldsForAssertion
        # TODO underscore on next line?
        message = self.sipMessageClassUnderTest.new_for_attributes(start_line=MalformedSIPStartLine.new_parsed_from('Malformed start line'), content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_one_big_header_string(self):
        header_fields = self.oneBigHeaderStringForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(start_line=MalformedSIPStartLine.new_parsed_from('Malformed start line'), content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_header_field_strings(self):
        header_fields = self.listOfHeaderFieldStringsForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(start_line=MalformedSIPStartLine.new_parsed_from('Malformed start line'), content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(start_line=MalformedSIPStartLine.new_parsed_from('Malformed start line'), content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(start_line=MalformedSIPStartLine.new_parsed_from('Malformed start line'), content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(message)
