import inspect
from abstractSIPMessageTestCase import AbstractSIPMessageTestCase
from sipmessaging import SIPHeader
import unittest

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
    def statusCode(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def reasonPhrase(self):
        raise NotImplementedError('call to abstract method ' + inspect.stack()[0][3])

    @property
    def sipMethodString(self):
        # For a response, this is just for building the header strings.
        return "INVITE"

    @property
    def canonicalStartLineStrings(self):
        # TODO - Moar???
        return ["SIP/2.0 " + str(self.statusCode) + " " + self.reasonPhrase]

    def runAssertionsForSIPMessage(self, aSIPMessage):
        super(AbstractSIPResponseTestCase, self).runAssertionsForSIPMessage(aSIPMessage)
        self.assertTrue(aSIPMessage.isValid)
        self.assertFalse(aSIPMessage.isRequest)
        self.assertTrue(aSIPMessage.isResponse)
        self.assertFalse(aSIPMessage.isMalformed)
        self.assertFalse(aSIPMessage.startLine.isRequest)
        self.assertTrue(aSIPMessage.startLine.isResponse)
        self.assertFalse(aSIPMessage.startLine.isMalformed)
        self.assertEqual(self.canonicalStartLineStrings[0], aSIPMessage.startLine.rawString)
        self.assertEqual(self.statusCode, aSIPMessage.startLine.statusCode)
        self.assertEqual(self.reasonPhrase, aSIPMessage.startLine.reasonPhrase)

    def run_test_parsing(self):
        for messageString in self.canonicalStrings:
            response = self.sipMessageClassUnderTest.newParsedFrom(messageString)
            self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_header_fields(self):
        headerFields = self.listOfHeaderFieldsForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_one_big_header_string(self):
        headerFields = self.oneBigHeaderStringForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_one_big_header_string_with_folding(self):
        headerFields = self.oneBigHeaderStringWithFoldingForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_header_field_strings(self):
        headerFields = self.listOfHeaderFieldStringsForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        response = self.sipMessageClassUnderTest.newForAttributes(statusCode=self.statusCode, reasonPhrase=self.reasonPhrase, content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(response)
