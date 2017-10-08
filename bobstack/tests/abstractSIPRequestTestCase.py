from abstractSIPMessageTestCase import AbstractSIPMessageTestCase
from ..sipmessaging import SIPHeader
import inspect


class AbstractSIPRequestTestCase(AbstractSIPMessageTestCase):
    @property
    def sipMethodString(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMessageClassUnderTest(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalStartLineStrings(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMethodString(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def canonicalStartLineStrings(self):
        # TODO - Moar???
        return [self.sipMethodString + " sip:example.com SIP/2.0"]

    def runAssertionsForSIPMessage(self, a_sip_message):
        super(AbstractSIPRequestTestCase, self).runAssertionsForSIPMessage(a_sip_message)
        self.assertTrue(a_sip_message.is_valid)
        self.assertTrue(a_sip_message.is_request)
        self.assertFalse(a_sip_message.is_response)
        self.assertFalse(a_sip_message.is_malformed)
        self.assertTrue(a_sip_message.start_line.is_request)
        self.assertFalse(a_sip_message.start_line.is_response)
        self.assertFalse(a_sip_message.start_line.is_malformed)
        self.assertEqual(self.sipMethodString, a_sip_message.start_line.sip_method)
        self.assertEqual('sip:example.com', a_sip_message.start_line.request_uri)
        self.assertEqual(self.canonicalStartLineStrings[0], a_sip_message.start_line.raw_string)

    def run_test_parsing(self):
        for message_string in self.canonicalStrings:
            request = self.sipMessageClassUnderTest.new_parsed_from(message_string)
            self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_header_fields(self):
        header_fields = self.listOfHeaderFieldsForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_one_big_header_string(self):
        header_fields = self.oneBigHeaderStringForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_one_big_header_string_with_folding(self):
        header_fields = self.oneBigHeaderStringWithFoldingForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_header_field_strings(self):
        header_fields = self.listOfHeaderFieldStringsForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        request = self.sipMessageClassUnderTest.new_for_attributes(sip_method=self.sipMethodString, request_uri='sip:example.com', content='Foo Content', header=SIPHeader.new_for_attributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(request)



