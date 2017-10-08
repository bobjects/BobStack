from abstractMalformedSIPMessageTestCase import AbstractMalformedSIPMessageTestCase
# import sys
# # sys.path.append("..")
from ..sipmessaging import MalformedSIPMessage


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
        self.assertFalse(a_sip_response.is_known)
        self.assertTrue(a_sip_response.is_unknown)
        self.assertFalse(a_sip_response.is_ack_request)
        self.assertFalse(a_sip_response.is_bye_request)
        self.assertFalse(a_sip_response.is_cancel_request)
        self.assertFalse(a_sip_response.is_info_request)
        self.assertFalse(a_sip_response.is_invite_request)
        self.assertFalse(a_sip_response.is_notify_request)
        self.assertFalse(a_sip_response.is_prack_request)
        self.assertFalse(a_sip_response.is_publish_request)
        self.assertFalse(a_sip_response.is_message_request)
        self.assertFalse(a_sip_response.is_options_request)
        self.assertFalse(a_sip_response.is_refer_request)
        self.assertFalse(a_sip_response.is_register_request)
        self.assertFalse(a_sip_response.is_subscribe_request)
        self.assertFalse(a_sip_response.is_update_request)

