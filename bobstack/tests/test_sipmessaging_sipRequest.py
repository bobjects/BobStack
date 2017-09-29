from abstractSIPRequestTestCase import AbstractSIPRequestTestCase
import sys
sys.path.append("..")
from sipmessaging import UnknownSIPRequest
from sipmessaging import ACKSIPRequest
from sipmessaging import BYESIPRequest
from sipmessaging import CANCELSIPRequest
from sipmessaging import INFOSIPRequest
from sipmessaging import INVITESIPRequest
from sipmessaging import NOTIFYSIPRequest
from sipmessaging import PRACKSIPRequest
from sipmessaging import PUBLISHSIPRequest
from sipmessaging import MESSAGESIPRequest
from sipmessaging import OPTIONSSIPRequest
from sipmessaging import REFERSIPRequest
from sipmessaging import REGISTERSIPRequest
from sipmessaging import SUBSCRIBESIPRequest
from sipmessaging import UPDATESIPRequest


class TestUnknownSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "UNKNOWN"

    @property
    def sipMessageClassUnderTest(self):
        return UnknownSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestUnknownSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertFalse(a_sip_request.isKnown)
        self.assertTrue(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestOPTIONSSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "OPTIONS"

    @property
    def sipMessageClassUnderTest(self):
        return OPTIONSSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestOPTIONSSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertTrue(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestACKSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "ACK"

    @property
    def sipMessageClassUnderTest(self):
        return ACKSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestACKSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertTrue(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestBYESIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "BYE"

    @property
    def sipMessageClassUnderTest(self):
        return BYESIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestBYESIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertTrue(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestCANCELSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "CANCEL"

    @property
    def sipMessageClassUnderTest(self):
        return CANCELSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestCANCELSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertTrue(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestINFOSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "INFO"

    @property
    def sipMessageClassUnderTest(self):
        return INFOSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestINFOSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertTrue(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestINVITESIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "INVITE"

    @property
    def sipMessageClassUnderTest(self):
        return INVITESIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestINVITESIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertTrue(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestNOTIFYSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "NOTIFY"

    @property
    def sipMessageClassUnderTest(self):
        return NOTIFYSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestNOTIFYSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertTrue(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestPRACKSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "PRACK"

    @property
    def sipMessageClassUnderTest(self):
        return PRACKSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestPRACKSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertTrue(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestPUBLISHSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "PUBLISH"

    @property
    def sipMessageClassUnderTest(self):
        return PUBLISHSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestPUBLISHSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertTrue(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestMESSAGESIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "MESSAGE"

    @property
    def sipMessageClassUnderTest(self):
        return MESSAGESIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestMESSAGESIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertTrue(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestREFERSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "REFER"

    @property
    def sipMessageClassUnderTest(self):
        return REFERSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestREFERSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertTrue(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestREGISTERSIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "REGISTER"

    @property
    def sipMessageClassUnderTest(self):
        return REGISTERSIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestREGISTERSIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertTrue(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestSUBSCRIBESIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "SUBSCRIBE"

    @property
    def sipMessageClassUnderTest(self):
        return SUBSCRIBESIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestSUBSCRIBESIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertTrue(a_sip_request.isSUBSCRIBERequest)
        self.assertFalse(a_sip_request.isUPDATERequest)


class TestUPDATESIPRequest(AbstractSIPRequestTestCase):
    @property
    def sipMethodString(self):
        return "UPDATE"

    @property
    def sipMessageClassUnderTest(self):
        return UPDATESIPRequest

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

    def runAssertionsForSIPMessage(self, a_sip_request):
        super(TestUPDATESIPRequest, self).runAssertionsForSIPMessage(a_sip_request)
        self.assertTrue(a_sip_request.isKnown)
        self.assertFalse(a_sip_request.isUnknown)
        self.assertFalse(a_sip_request.isACKRequest)
        self.assertFalse(a_sip_request.isBYERequest)
        self.assertFalse(a_sip_request.isCANCELRequest)
        self.assertFalse(a_sip_request.isINFORequest)
        self.assertFalse(a_sip_request.isINVITERequest)
        self.assertFalse(a_sip_request.isNOTIFYRequest)
        self.assertFalse(a_sip_request.isPRACKRequest)
        self.assertFalse(a_sip_request.isPUBLISHRequest)
        self.assertFalse(a_sip_request.isMESSAGERequest)
        self.assertFalse(a_sip_request.isOPTIONSRequest)
        self.assertFalse(a_sip_request.isREFERRequest)
        self.assertFalse(a_sip_request.isREGISTERRequest)
        self.assertFalse(a_sip_request.isSUBSCRIBERequest)
        self.assertTrue(a_sip_request.isUPDATERequest)
