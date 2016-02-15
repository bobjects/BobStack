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

    def runAssertionsForSIPMessage(self, aSIPMessage):
        super(AbstractMalformedSIPMessageTestCase, self).runAssertionsForSIPMessage(aSIPMessage)
        self.assertFalse(aSIPMessage.isValid)
        self.assertFalse(aSIPMessage.isRequest)
        self.assertFalse(aSIPMessage.isResponse)
        self.assertTrue(aSIPMessage.isMalformed)
        self.assertFalse(aSIPMessage.startLine.isRequest)
        self.assertFalse(aSIPMessage.startLine.isResponse)
        self.assertTrue(aSIPMessage.startLine.isMalformed)
        self.assertEqual(self.canonicalStartLineStrings[0], aSIPMessage.startLine.rawString)

    def run_test_parsing(self):
        for messageString in self.canonicalStrings:
            message = self.sipMessageClassUnderTest.newParsedFrom(messageString)
            self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_header_fields(self):
        headerFields = self.listOfHeaderFieldsForAssertion
        # TODO underscore on next line?
        message = self.sipMessageClassUnderTest._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_one_big_header_string(self):
        headerFields = self.oneBigHeaderStringForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_header_field_strings(self):
        headerFields = self.listOfHeaderFieldStringsForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_field_names_and_values(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(message)

    def run_test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        headerFields = self.listOfHeaderFieldNamesAndValuesUsingPropertyDictForAssertion
        message = self.sipMessageClassUnderTest._newForAttributes(startLine=MalformedSIPStartLine.newParsedFrom('Malformed start line'), content='Foo Content', header=SIPHeader.newForAttributes(headerFields=headerFields))
        self.runAssertionsForSIPMessage(message)
