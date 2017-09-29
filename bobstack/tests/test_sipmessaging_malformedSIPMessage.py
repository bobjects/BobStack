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

    def runAssertionsForSIPMessage(self, a_sip_response):
        super(TestMalformedSipMessage, self).runAssertionsForSIPMessage(a_sip_response)
        self.assertFalse(a_sip_response.isKnown)
        self.assertTrue(a_sip_response.isUnknown)
        self.assertFalse(a_sip_response.isACKRequest)
        self.assertFalse(a_sip_response.isBYERequest)
        self.assertFalse(a_sip_response.isCANCELRequest)
        self.assertFalse(a_sip_response.isINFORequest)
        self.assertFalse(a_sip_response.isINVITERequest)
        self.assertFalse(a_sip_response.isNOTIFYRequest)
        self.assertFalse(a_sip_response.isPRACKRequest)
        self.assertFalse(a_sip_response.isPUBLISHRequest)
        self.assertFalse(a_sip_response.isMESSAGERequest)
        self.assertFalse(a_sip_response.isOPTIONSRequest)
        self.assertFalse(a_sip_response.isREFERRequest)
        self.assertFalse(a_sip_response.isREGISTERRequest)
        self.assertFalse(a_sip_response.isSUBSCRIBERequest)
        self.assertFalse(a_sip_response.isUPDATERequest)

