import inspect
from abstractSIPMessageTestCase import AbstractSIPMessageTestCase
from sipmessaging import SIPHeader


class AbstractSIPResponseTestCase(AbstractSIPMessageTestCase):
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
    def status_code(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def reason_phrase(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMethodString(self):
        # For a response, this is just for building the header strings.
        return "INVITE"

    @property
    def canonicalStartLineStrings(self):
        # TODO - Moar???
        return ["SIP/2.0 " + str(self.status_code) + " " + self.reason_phrase]

    def runAssertionsForSIPMessage(self, a_sip_message):
        super(AbstractSIPResponseTestCase, self).runAssertionsForSIPMessage(a_sip_message)
        self.assertTrue(a_sip_message.isValid)
        self.assertFalse(a_sip_message.isRequest)
        self.assertTrue(a_sip_message.isResponse)
        self.assertFalse(a_sip_message.isMalformed)
        self.assertFalse(a_sip_message.start_line.isRequest)
        self.assertTrue(a_sip_message.start_line.isResponse)
        self.assertFalse(a_sip_message.start_line.isMalformed)
        self.assertEqual(self.canonicalStartLineStrings[0], a_sip_message.start_line.rawString)
        self.assertEqual(self.status_code, a_sip_message.start_line.status_code)
        self.assertEqual(self.reason_phrase, a_sip_message.start_line.reason_phrase)

    def run_test_parsing(self):
        for message_string in self.canonicalStrings:
            response = self.sipMessageClassUnderTest.newParsedFrom(message_string)
            self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_header_fields(self):
        header_fields = self.listOfHeaderFieldsForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_one_big_header_string(self):
        header_fields = self.oneBigHeaderStringForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_one_big_header_string_with_folding(self):
        header_fields = self.oneBigHeaderStringWithFoldingForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_header_field_strings(self):
        header_fields = self.listOfHeaderFieldStringsForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        header_fields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(status_code=self.status_code, reason_phrase=self.reason_phrase, content='Foo Content', header=SIPHeader.newForAttributes(header_fields=header_fields))
        self.runAssertionsForSIPMessage(response)
