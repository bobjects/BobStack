from ..sipmessaging import SIPURI
from ..sipmessaging import ViaSIPHeaderField
from ..sipmessaging import ContentLengthSIPHeaderField
from ..sipmessaging import RouteSIPHeaderField
from ..sipmessaging import RecordRouteSIPHeaderField
from ..sipmessaging import MaxForwardsSIPHeaderField
from ..sipmessaging import ServerSIPHeaderField
from ..sipmessaging import SIPResponse
from ..siptransport import ConnectedSIPMessage
from sipEntity import SIPEntity
from sipEntityExceptions import DropMessageSIPEntityException, DropMessageAndDropConnectionSIPEntityException, SendResponseSIPEntityException

'''
Proxy behavior is defined in RFC3261, section 16, https://tools.ietf.org/html/rfc3261#section-16
Behavior specific to stateless proxies is defined in Section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
'''


class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def received_valid_connected_request_event_handler(self, received_connected_sip_message):
        print "Stateless proxy " + str(self.transports[0].bind_address) + " request payload...\n" + str(received_connected_sip_message.sip_message.raw_string)
        try:
            request_arrival_transport_connection_id = self.transport_connection_id_for_request(received_connected_sip_message)
            self.validate_request(received_connected_sip_message)
            connected_sip_message_to_send = self.create_connected_sip_message_to_send_for_request(received_connected_sip_message)
            self.preprocess_routing_information_for_request(connected_sip_message_to_send)
            target_uri = self.determine_target_for_request(connected_sip_message_to_send)
            self.forward_request_to_target(connected_sip_message_to_send, target_uri=target_uri, transport_id_for_header=request_arrival_transport_connection_id)
        except DropMessageSIPEntityException:
            pass  # just let it drop.
        except DropMessageAndDropConnectionSIPEntityException:
            received_connected_sip_message.disconnect()
        except SendResponseSIPEntityException as ex:
            self.send_error_response_for_request(received_connected_sip_message, status_code_integer=ex.status_code, reason_phrase_string=ex.reason_phrase, description_string=ex.description)

    def received_valid_connected_response_event_handler(self, received_connected_sip_message):
        '''
        Stateful proxy response processing is defined in RFC3261 section 16.7.  But for stateless proxy behavior, see
        notes toward the bottom of section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
        '''
        print "Stateless proxy " + str(self.transports[0].bind_address) + " response payload...\n" + str(received_connected_sip_message.sip_message.raw_string)
        try:
            self.validate_response(received_connected_sip_message)
            if self.response_should_be_forwarded(received_connected_sip_message):
                connected_sip_message_to_send = self.create_connected_sip_message_to_send_for_response(received_connected_sip_message)
                self.remove_via_for_response(connected_sip_message_to_send)
                self.rewrite_record_route_for_response(connected_sip_message_to_send)
                target_uri = self.determine_target_for_response(connected_sip_message_to_send)
                self.forward_response_to_target(connected_sip_message_to_send, target_uri=target_uri)
        except DropMessageSIPEntityException:
            pass
        except DropMessageAndDropConnectionSIPEntityException:
            received_connected_sip_message.disconnect()
        except SendResponseSIPEntityException as ex:
            self.send_error_response_for_response(received_connected_sip_message, status_code_integer=ex.status_code, reason_phrase_string=ex.reason_phrase, description_string=ex.description)

    @staticmethod
    def transport_connection_id_for_request(received_connected_sip_message):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.1
        In some circumstances, a proxy MAY forward requests using stateful
       transports (such as TCP) without being transaction-stateful.  For
       instance, a proxy MAY forward a request from one TCP connection to
       another transaction statelessly as long as it places enough
       information in the message to be able to forward the response down
       the same connection the request arrived on.
        '''
        return received_connected_sip_message.connection.id

    @staticmethod
    def validate_request(received_connected_sip_message):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.3
        Validate the request
             - is_malformed is False
             - Check for a merged request (i.e. 482 (Loop Detected))
             - Check the request URI scheme, to ensure that we understand it (i.e. "sip" or "sips") 416 (Unsupported URI Scheme)
             - Check Max-Forwards.  If 0, don't forward the request, 483 (Too Many Hops)
             - (optional) Loop check.  Via header with sent-by value that's already been placed into previous requests by us
                - Maybe only appropriate for stateful proxy.
             - Proxy-Require test - 420 (Bad Extension)
             - Proxy-Authorization check -
        '''
        sip_message = received_connected_sip_message.sip_message
        if sip_message.is_malformed:
            # TODO - do we need to drop the connection if malformed?  What does the RFC say about that?
            raise DropMessageSIPEntityException(description_string='Received SIP message was malformed.')
        # TODO - we instantiate a first-class SIPURI object here.  We probably want to do that in the start line object instead.
        request_uri = SIPURI.new_parsed_from(sip_message.request_uri)
        if request_uri.scheme not in ['sip', 'sips']:
            raise SendResponseSIPEntityException(status_code_integer=416, reason_phrase_string='Unsupported URI Scheme')
        if sip_message.max_forwards is not None:
            if sip_message.max_forwards <= 0:
                raise SendResponseSIPEntityException(status_code_integer=483, reason_phrase_string='Too many hops')
        # TODO - for now, skip the optional loop detection.
        # TODO - for now, skip the Proxy-Require header field check.
        #    We will flesh out Proxy-Require once we know for sure which features we handle.
        # TODO - for now, we don't do authentication.  When we do, the authorization check will be here.
        # TODO - "If any of these checks fail, the element MUST behave as a user agent server (see Section 8.2) and respond with an error code."

    @staticmethod
    def create_connected_sip_message_to_send_for_request(received_connected_sip_message):
        # We do a total copy of the sip_message.  The connection will be replaced later.
        sip_message = received_connected_sip_message.sip_message.deep_copy
        return ConnectedSIPMessage(received_connected_sip_message.connection, sip_message)

    def preprocess_routing_information_for_request(self, connected_sip_message_to_send):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.4

        '''
        # TODO - for now, skip strict route stuff in the first paragraph of 16.4
        sip_message = connected_sip_message_to_send.sip_message
        request_uri = SIPURI.new_parsed_from(sip_message.request_uri)
        maddr = request_uri.parameter_named('maddr')
        if maddr:
            # TODO - for now, skip the maddr processing step.
            pass
        route_uris = sip_message.route_uris
        if route_uris:
            if self.sip_uri_matches_us(route_uris[0]):
                # TODO - remove first route header, because it matches us.
                # TODO - need to test that remove_first_header_field_of_class() works correctly.  Header field tests should be written for that.
                sip_message.remove_first_header_field_of_class(RouteSIPHeaderField)
                # TODO:  This line is a work-around for a problem that we really
                # need to address: when you hack a header or header field value, that
                # does not clear the SIPMessage's raw_string.  Fixing that is not trivial,
                # considering that we observe good layering practices in the message - header - hf
                # object complex.  We will probably need to use events for that.  Don't blow this
                # off, but for now, just manually clear the raw_string.
                sip_message.clear_raw_string()

    def determine_target_for_request(self, connected_sip_message_to_send):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.5
        Special consideration for stateless proxies explained in section 16.11
        - Choose only one target (not forking), based on time-invariant stuff.
        '''
        sip_message = connected_sip_message_to_send.sip_message
        request_uri = SIPURI.new_parsed_from(sip_message.request_uri)
        maddr = request_uri.parameter_named('maddr')
        if maddr:
            return request_uri
        if not self.sip_uri_matches_us(request_uri):
            return request_uri
        # TODO - we are responsible for this request.  We will have a registrar
        # or location service, probably implemented using the Strategy pattern,
        # but for now, let's just make a degenerate behavior, by answering a 404.  We will
        # implement that location service later.  Also allow other developers to write their
        # own Strategy objects.
        raise SendResponseSIPEntityException(status_code_integer=404, reason_phrase_string='Not Found')

    def forward_request_to_target(self, connected_sip_message_to_send, target_uri=None, transport_id_for_header=None):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.6
        Special consideration for stateless proxies explained in section 16.11
        - The unique branch id must be invariant for requests with identical headers.
        - Item 10 will send the forwarded message directly to a transport_connection, not transaction.
        '''
        sip_message = connected_sip_message_to_send.sip_message
        # TODO: in progress
        # 1. Copy request
        #   (already copied it)
        # 2.  Update the Request-URI
        # TODO: need to remove any URI parameters that are not allowed in a Request URI.
        # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
        if target_uri:
            sip_message.start_line.request_uri = target_uri.raw_string
        # 3.  Update the Max-Forwards header field
        if sip_message.max_forwards is not None:
            # TODO:  When you use -= 1 on an integer sip header field's integer_value parameter, does that work?  Need to write a test.
            sip_message.header.max_forwards_header_field.integer_value -= 1
        else:
            # TODO: inserting a header field - we should make a method that inserts it using an aesthetically-pleasing order
            # relative to other header fields.  Each header field concrete subclass would have an integer sort attribute for that.
            sip_message.header.add_header_field(MaxForwardsSIPHeaderField.new_for_integer_value(70))
        # 4.  Optionally add a Record-route header field value
        # TODO: is this the best way to get the URI host?
        # Are record-route header fields only used for INVITE?  Should we only do this if it's an INVITE?
        #    Answer:  No.  See RFC3261 16.6  point 4
        # TODO: sip or sips scheme?  Should that be derived from the transport_connection?  For now, hard-code to 'sip'
        record_route_uri = SIPURI.new_for_attributes(host=self.transports[0].bind_address, port=self.transports[0].bind_port, scheme='sip', parameter_names_and_value_strings={'lr': None})
        record_route_header_field = RecordRouteSIPHeaderField.new_for_attributes(record_route_uri)
        if transport_id_for_header:
            # Do we want to put that state into this header or the Via?
            #    Answer:  we want it here.  See RFC3261 16.6  point 4
            record_route_header_field.parameter_named_put('bobstackTransportID', transport_id_for_header)
        sip_message.header.add_header_field_before_header_fields_of_same_class(record_route_header_field)

        # 5.  Optionally add additional header fields
        # TODO: make the server header field a user-settable parameter.
        sip_message.header.add_header_field(ServerSIPHeaderField.new_for_value_string('BobStack'))

        # 6.  Postprocess routing information
        route_uris = sip_message.header.route_uris
        if route_uris:
            if 'lr' not in route_uris[0].parameter_names:
                # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
                sip_message.header.add_header_field_after_header_fields_of_same_class(RouteSIPHeaderField.new_for_attributes(SIPURI.new_parsed_from(sip_message.start_line.request_uri)))
                sip_message.start_line.request_uri = route_uris[0].raw_string
                # TODO: Is the class actually the same object, considering that we're accessing it from a different directory?  Trap for young players.
                # No, as a matter of fact, it is not the same object, and that's a problem.  We've worked around it over there,
                # but we need to do better.
                sip_message.header.remove_first_header_field_of_class(RouteSIPHeaderField)
                uri_to_determine_next_hop = sip_message.request_uri
            else:
                uri_to_determine_next_hop = route_uris[0]
        else:
            # TODO: seriously, we need to make start lines use first-class SIPURIs.
            uri_to_determine_next_hop = SIPURI.new_parsed_from(sip_message.request_uri)

        # 7.  Determine the next-hop address, port, and transport
        next_hop_connected_transport_connection = self.connected_transport_connection_for_sip_uri(uri_to_determine_next_hop)
        if not next_hop_connected_transport_connection:
            # TODO:  we could not connect to the next-hop.  Return some error code.  Which error code and reason phrase?  400 and could not connect are NOT correct.
            raise SendResponseSIPEntityException(status_code_integer=400, reason_phrase_string='Could not connect')

        # 8.  Add a Via header field value
        # TODO:  For now, don't do the loop / spiral detection stuff.
        sip_message.header.add_header_field_before_header_fields_of_same_class(self.new_via_header_field_for_sip_message(sip_message))

        # 9.  Add a Content-Length header field if necessary
        # TODO: if the target transport is stream-oriented, e.g. TLS or TCP, and the message has no Content-Length: header field, add one.
        # TODO: So we'll need to wait until step 7 is done, to know the transport.
        if not sip_message.header.content_length_header_field:
            if next_hop_connected_transport_connection.is_stateful:
                # TODO: if the target transport is stream-oriented, e.g. TLS or TCP, and the message has no Content-Length: header field, add one.
                sip_message.header.add_header_field(self.new_content_length_header_field_for_sip_message(sip_message))

        # TODO:  This line is a work-around for a problem that we really
        # need to address: when you hack a header or header field value, that
        # does not clear the SIPMessage's raw_string.  Fixing that is not trivial,
        # considering that we observe good layering practices in the message - header - hf
        # object complex.  We will probably need to use events for that.  Don't blow this
        # off, but for now, just manually clear the raw_string.
        sip_message.clear_raw_string()

        # 10. Forward the new request
        # TODO:  exception handling?
        next_hop_connected_transport_connection.send_message(sip_message)

        # 11. Set timer C - not applicable for stateless.  Huzzah!

    def connected_transport_connection_for_sip_uri(self, a_sip_uri):
        if not self.transports:
            return None
        # 7.  Determine the next-hop address, port, and transport
        # TODO:  This is about determining the target set.
        # TODO:  Gotta study RFC3263 (i.e. reference 4 of 3261)
        # RFC3263 is mainly about DNS SRV and NAPTR.  We don't actually want to deal with
        # DNS related stuff now, just use our dotted IPs.  There is also discussion (section 4
        # about choosing transport.
        # TODO:  next: get the address and port, just using the dotted IP address for now.
        # TODO:  because we are just assuming dotted IP addresses for right now, we just assume that host is the dotted IP address,
        # and we do not attempt to resolve it using DNS, SRV, NAPTR, etc.
        # TODO:  We also need to derive / create the next hop transport
        next_hop_address = a_sip_uri.host
        next_hop_port = a_sip_uri.derived_port
        # TODO:  Not yet done.  We will return an existing protocol that matches the uri's host, port, and is appropriate
        # for the uri's scheme.  If it doesn't exist, we will create a new one and connect it.  If connection fails, we will
        # return None.
        # TODO:  We also need to check that the transport is compatible with the URI's scheme.
        existing_connection = self.transports[0].connection_with_address_and_port(next_hop_address, next_hop_port)
        if existing_connection:
            return existing_connection
        else:
            # TODO:  Need to make (and test) exception handler in case the connection could not be made.
            return self.transports[0].connect_to_address_and_port(next_hop_address, next_hop_port)

    def new_via_header_field_for_sip_message(self, a_sip_message):
        # TODO:  WE NEED TO USE THE TARGET SET ATTRIBUTES!  SEE "7." ABOVE!
        # TODO:  Need to do transport string as well.
        answer = ViaSIPHeaderField.new_for_attributes()
        answer.host = self.our_host
        answer.port = self.our_port
        answer.transport = 'UDP'
        answer.generate_invariant_branch_for_sip_header(a_sip_message.header)
        return answer

    @staticmethod
    def new_content_length_header_field_for_sip_message(a_sip_message):
        return ContentLengthSIPHeaderField.new_for_integer_value(len(a_sip_message.body))

    @property
    def our_host(self):
        # TODO: This is very simplistic for now.
        try:
            return self.home_domains[0]
        except IndexError:
            return '127.0.0.1'

    @property
    def our_port(self):
        # TODO: This is very simplistic for now.
        try:
            return self.transports[0].bind_port
        except IndexError:
            return 5060

    def sip_uri_matches_us(self, a_sip_uri):
        # TODO - we will also need to verify match of transport protocol and port, right?
        return a_sip_uri.host in self.home_domains

    @staticmethod
    def send_error_response_for_request(received_connected_sip_message, status_code_integer=500, reason_phrase_string='Server Error', description_string='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # Response header fields to include in a response are documented in RFC3261 8.2.6
        sip_request_replying_to = received_connected_sip_message.sip_message
        connection = received_connected_sip_message.connection
        sip_response = SIPResponse.new_for_attributes(status_code=status_code_integer, reason_phrase=reason_phrase_string)
        if sip_request_replying_to.header.to_tag:
            sip_response.header.add_header_field(sip_request_replying_to.header.to_header_field)
        else:
            hf = sip_request_replying_to.header.to_header_field.deep_copy
            # TODO:  See RFC3261 section 8.2.7 last point - tag must be invariant for identical To headers.  So need to write a method to generate an invariant tag.
            hf.generate_tag()
            sip_response.header.add_header_field(hf)
        sip_response.header.add_header_field(sip_request_replying_to.header.from_header_field)
        sip_response.header.add_header_field(sip_request_replying_to.header.call_id_header_field)
        sip_response.header.add_header_field(sip_request_replying_to.header.cseq_header_field)
        sip_response.header.add_header_fields(sip_request_replying_to.via_header_fields)
        sip_response.header.add_header_field(ContentLengthSIPHeaderField.new_for_integer_value(0))
        sip_response.clear_raw_string()
        connection.send_message(sip_response)

    @staticmethod
    def transport_connection_id_from_response(received_connected_sip_message):
        route_header_fields = received_connected_sip_message.sip_message.header.route_header_fields
        if route_header_fields:
            return route_header_fields[0].parameter_named('bobstackTransportID')
        return None

    def response_send_transport_connection_from_connection_id(self, connection_id_string):
        if connection_id_string:
            # TODO:  We will probably need to iterate over the transports.
            return self.transports[0].connection_with_id(connection_id_string)
        return None

    def validate_response(self, received_connected_sip_message):
        # Stateless proxy response processing behavior is simple.
        # We just check to see if we put in the first Via header,
        # and if so, remove it.
        # TODO:  Need to verify transport string as well.
        try:
            via_hf = received_connected_sip_message.sip_message.via_header_fields[0]
            if via_hf.host == self.our_host and via_hf.port == self.our_port:
                return
            else:
                raise DropMessageSIPEntityException(description_string='Received SIP response was not meant for us.')
        except IndexError:
            raise DropMessageSIPEntityException(description_string='Received SIP response was not meant for us.')

    @staticmethod
    def response_should_be_forwarded(received_connected_sip_message):
        # We remove the top Via, and forward to the second Via, if it exists.
        try:
            via_hf = received_connected_sip_message.sip_message.via_header_fields[1]
            return via_hf.host is not None and via_hf.port is not None
        except IndexError:
            return False

    @staticmethod
    def create_connected_sip_message_to_send_for_response(received_connected_sip_message):
        # We do a total copy of the sip_message.  The connection will be replaced later.
        sip_message = received_connected_sip_message.sip_message.deep_copy
        return ConnectedSIPMessage(received_connected_sip_message.connection, sip_message)

    @staticmethod
    def remove_via_for_response(connected_sip_message_to_send):
        connected_sip_message_to_send.sip_message.header.remove_first_header_field_of_class(ViaSIPHeaderField)
        # TODO:  This line is a work-around for a problem that we really
        # need to address: when you hack a header or header field value, that
        # does not clear the SIPMessage's raw_string.  Fixing that is not trivial,
        # considering that we observe good layering practices in the message - header - hf
        # object complex.  We will probably need to use events for that.  Don't blow this
        # off, but for now, just manually clear the raw_string.
        connected_sip_message_to_send.sip_message.clear_raw_string()

    def rewrite_record_route_for_response(self, connected_sip_message_to_send):
        # Not applicable for stateless proxies, I guess.
        pass

    @staticmethod
    def determine_target_for_response(connected_sip_message_to_send):
        try:
            via_hf = connected_sip_message_to_send.sip_message.via_header_fields[0]
            return via_hf.as_sip_uri
        except IndexError:
            raise DropMessageSIPEntityException(description_string='Received SIP response had no target Via header.')

    def forward_response_to_target(self, connected_sip_message_to_send, target_uri=None):
        request_arrival_transport_connection_id = self.transport_connection_id_from_response(connected_sip_message_to_send)
        # TODO:  For stateless proxies, do we want to derive the transport connection from the Route header like this:
        # transport_connection = self.response_send_transport_connection_from_connection_id(request_arrival_transport_connection_id)
        # TODO:  Or from the target_uri like this:
        transport_connection = self.connected_transport_connection_for_sip_uri(target_uri)
        if not transport_connection:
            # TODO:  we could not connect.  Just drop the response.
            raise DropMessageSIPEntityException
        # 10. Forward the new response
        # TODO:  exception handling?
        transport_connection.send_message(connected_sip_message_to_send.sip_message)

    @staticmethod
    def send_error_response_for_response(received_connected_sip_message, status_code_integer=500, reason_phrase_string='Server Error', description_string='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # TODO
        raise Exception('not yet implemented')

