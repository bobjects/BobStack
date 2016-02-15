from unittest import TestCase
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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestUnknownSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertFalse(aSIPRequest.isKnown)
        self.assertTrue(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestOPTIONSSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertTrue(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestACKSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertTrue(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestBYESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertTrue(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestCANCELSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertTrue(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestINFOSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertTrue(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestINVITESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertTrue(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestNOTIFYSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertTrue(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestREFERSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertTrue(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestREGISTERSIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertTrue(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestSUBSCRIBESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertTrue(aSIPRequest.isSUBSCRIBERequest)
        self.assertFalse(aSIPRequest.isUPDATERequest)


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

    def test_rendering_from_list_of_header_field_strings(self):
        self.run_test_rendering_from_list_of_header_field_strings()

    def test_rendering_from_list_of_field_names_and_values(self):
        self.run_test_rendering_from_list_of_field_names_and_values()

    def test_rendering_from_list_of_field_names_and_values_using_property_dict(self):
        self.run_test_rendering_from_list_of_field_names_and_values_using_property_dict()

    def runAssertionsForSIPMessage(self, aSIPRequest):
        super(TestUPDATESIPRequest, self).runAssertionsForSIPMessage(aSIPRequest)
        self.assertTrue(aSIPRequest.isKnown)
        self.assertFalse(aSIPRequest.isUnknown)
        self.assertFalse(aSIPRequest.isACKRequest)
        self.assertFalse(aSIPRequest.isBYERequest)
        self.assertFalse(aSIPRequest.isCANCELRequest)
        self.assertFalse(aSIPRequest.isINFORequest)
        self.assertFalse(aSIPRequest.isINVITERequest)
        self.assertFalse(aSIPRequest.isNOTIFYRequest)
        self.assertFalse(aSIPRequest.isOPTIONSRequest)
        self.assertFalse(aSIPRequest.isREFERRequest)
        self.assertFalse(aSIPRequest.isREGISTERRequest)
        self.assertFalse(aSIPRequest.isSUBSCRIBERequest)
        self.assertTrue(aSIPRequest.isUPDATERequest)
