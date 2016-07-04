from abstractMalformedSIPMessageTestCase import AbstractMalformedSIPMessageTestCase
import sys
sys.path.append("..")
from sipmessaging import MalformedSIPMessage


class TestMalformedSipMessage(AbstractMalformedSIPMessageTestCase):
    @property
    def sipMessageClassUnderTest(self):
        return MalformedSIPMessage

    def test_parsing(self):
        self.run_test_parsing()

    def test_rendering_from_list_of_header_fields(self):
        self.run_test_rendering_from_list_of_header_fields()

    def test_rendering_from_one_big_header_string(self):
        self.run_test_rendering_from_one_big_header_string()

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPResponse):
        super(TestMalformedSipMessage, self).runAssertionsForSIPMessage(aSIPResponse)
        self.assertFalse(aSIPResponse.isKnown)
        self.assertTrue(aSIPResponse.isUnknown)
        self.assertFalse(aSIPResponse.isACKRequest)
        self.assertFalse(aSIPResponse.isBYERequest)
        self.assertFalse(aSIPResponse.isCANCELRequest)
        self.assertFalse(aSIPResponse.isINFORequest)
        self.assertFalse(aSIPResponse.isINVITERequest)
        self.assertFalse(aSIPResponse.isNOTIFYRequest)
        self.assertFalse(aSIPResponse.isPRACKRequest)
        self.assertFalse(aSIPResponse.isPUBLISHRequest)
        self.assertFalse(aSIPResponse.isMESSAGERequest)
        self.assertFalse(aSIPResponse.isOPTIONSRequest)
        self.assertFalse(aSIPResponse.isREFERRequest)
        self.assertFalse(aSIPResponse.isREGISTERRequest)
        self.assertFalse(aSIPResponse.isSUBSCRIBERequest)
        self.assertFalse(aSIPResponse.isUPDATERequest)

