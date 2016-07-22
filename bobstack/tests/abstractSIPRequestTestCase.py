from abstractSIPMessageTestCase import AbstractSIPMessageTestCase
from sipmessaging import SIPHeader
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

    def runAssertionsForSIPMessage(self, aSIPMessage):
        super(AbstractSIPRequestTestCase, self).runAssertionsForSIPMessage(aSIPMessage)
        self.assertTrue(aSIPMessage.isValid)
        self.assertTrue(aSIPMessage.isRequest)
        self.assertFalse(aSIPMessage.isResponse)
        self.assertFalse(aSIPMessage.isMalformed)
        self.assertTrue(aSIPMessage.startLine.isRequest)
        self.assertFalse(aSIPMessage.startLine.isResponse)
        self.assertFalse(aSIPMessage.startLine.isMalformed)
        self.assertEqual(self.sipMethodString, aSIPMessage.startLine.sipMethod)
        self.assertEqual('sip:example.com', aSIPMessage.startLine.requestURI)
        self.assertEqual(self.canonicalStartLineStrings[0], aSIPMessage.startLine.rawString)

    def run_test_parsing(self):
        for messageString in self.canonicalStrings:
            request = self.sipMessageClassUnderTest.newParsedFrom(messageString)
            self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_header_fields(self):
        headerFields = self.listOfHeaderFieldsForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_one_big_header_string(self):
        headerFields = self.oneBigHeaderStringForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_one_big_header_string_with_folding(self):
        headerFields = self.oneBigHeaderStringWithFoldingForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_header_field_strings(self):
        headerFields = self.listOfHeaderFieldStringsForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        request = self.sipMessageClassUnderTest.newForAttributes(sipMethod=self.sipMethodString, requestURI='sip:example.com', content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(request)



