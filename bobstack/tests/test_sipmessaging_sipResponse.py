from abstractSIPResponseTestCase import AbstractSIPResponseTestCase
import sys
sys.path.append("..")
from sipmessaging import SIPResponse


class TestSIPResponse(AbstractSIPResponseTestCase):
    @property
    def statusCode(self):
        return 100

    @property
    def reasonPhrase(self):
        return "Trying"

    @property
    def sipMessageClassUnderTest(self):
        return SIPResponse

    def test_parsing(self):
        self.run_test_parsing()

    def test_rendering_from_list_of_header_fields(self):
        self.run_test_rendering_from_list_of_header_fields()

    def test_rendering_from_one_big_header_string(self):
        self.run_test_rendering_from_one_big_header_string()

    # TODO - skipping for now.
    # @unittest.skip("temporarily skipping...")
    def test_rendering_from_one_big_header_string_with_folding(self):
        self.run_test_rendering_from_one_big_header_string_with_folding()

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPResponse):
        super(TestSIPResponse, self).runAssertionsForSIPMessage(aSIPResponse)
        self.assertTrue(aSIPResponse.isKnown)
        self.assertFalse(aSIPResponse.isUnknown)
        self.assertFalse(aSIPResponse.isACKRequest)
        self.assertFalse(aSIPResponse.isBYERequest)
        self.assertFalse(aSIPResponse.isCANCELRequest)
        self.assertFalse(aSIPResponse.isINFORequest)
        self.assertFalse(aSIPResponse.isINVITERequest)
        self.assertFalse(aSIPResponse.isNOTIFYRequest)
        self.assertFalse(aSIPResponse.isNOTIFYRequest)
        self.assertFalse(aSIPResponse.isPRACKRequest)
        self.assertFalse(aSIPResponse.isPUBLISHRequest)
        self.assertFalse(aSIPResponse.isMESSAGERequest)
        self.assertFalse(aSIPResponse.isREFERRequest)
        self.assertFalse(aSIPResponse.isREGISTERRequest)
        self.assertFalse(aSIPResponse.isSUBSCRIBERequest)
        self.assertFalse(aSIPResponse.isUPDATERequest)
