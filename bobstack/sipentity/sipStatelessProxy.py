import sys
from hashlib import sha1
sys.path.append("../..")
from bobstack.sipmessaging import SIPURI
from bobstack.sipmessaging import ViaSIPHeaderField
from bobstack.sipmessaging import ContentLengthSIPHeaderField
from bobstack.sipmessaging import RouteSIPHeaderField
from bobstack.sipmessaging import RecordRouteSIPHeaderField
from bobstack.sipmessaging import MaxForwardsSIPHeaderField
from bobstack.sipmessaging import ServerSIPHeaderField
from bobstack.sipmessaging import SIPResponse
from bobstack.siptransport import ConnectedSIPMessage
from sipEntity import SIPEntity
from sipEntityExceptions import DropMessageSIPEntityException, DropMessageAndDropConnectionSIPEntityException, SendResponseSIPEntityException

'''
Proxy behavior is defined in RFC3261, section 16, https://tools.ietf.org/html/rfc3261#section-16
Behavior specific to stateless proxies is defined in Section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
'''


class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def receivedValidConnectedRequestEventHandler(self, receivedConnectedSIPMessage):
        print "Stateless proxy request payload - " + str(receivedConnectedSIPMessage)
        try:
            requestArrivalTransportConnectionID = self.transportConnectionIDForRequest(receivedConnectedSIPMessage)
            self.validateRequest(receivedConnectedSIPMessage)
            connectedSIPMessageToSend = self.createConnectedSIPMessageToSendForRequest(receivedConnectedSIPMessage)
            self.preprocessRoutingInformationForRequest(connectedSIPMessageToSend)
            targetURI = self.determineTargetForRequest(connectedSIPMessageToSend)
            self.forwardRequestToTarget(connectedSIPMessageToSend, targetURI=targetURI, transportIDForVia=requestArrivalTransportConnectionID)
        except DropMessageSIPEntityException:
            pass  # just let it drop.
        except DropMessageAndDropConnectionSIPEntityException:
            receivedConnectedSIPMessage.disconnect()
        except SendResponseSIPEntityException as ex:
            self.sendErrorResponseForRequest(receivedConnectedSIPMessage, statusCodeInteger=ex.statusCode, reasonPhraseString=ex.reasonPhrase, descriptionString=ex.description)

    def receivedValidConnectedResponseEventHandler(self, receivedConnectedSIPMessage):
        '''
        Stateful proxy response processing is defined in RFC3261 section 16.7.  But for stateless proxy behavior, see
        notes toward the bottom of section 16.11, https://tools.ietf.org/html/rfc3261#section-16.11
        '''
        print "Stateless proxy response payload - " + str(receivedConnectedSIPMessage)
        try:
            requestArrivalTransportConnectionID = self.transportConnectionIDForResponse(receivedConnectedSIPMessage)
            responseSendTransportConnection = self.responseSendTransportConnectionForConnectionID(requestArrivalTransportConnectionID)
            self.validateResponse(receivedConnectedSIPMessage)
            if self.responseShouldBeForwarded(receivedConnectedSIPMessage):
                connectedSIPMessageToSend = self.createConnectedSIPMessageToSendForResponse(receivedConnectedSIPMessage, responseSendTransportConnection)
                self.removeViaForResponse(connectedSIPMessageToSend)
                self.rewriteRecordRouteForResponse(connectedSIPMessageToSend)
                targetURI = self.determineTargetForResponse(connectedSIPMessageToSend)
                self.forwardResponseToTarget(connectedSIPMessageToSend, targetURI=targetURI)
        except DropMessageSIPEntityException:
            pass
        except DropMessageAndDropConnectionSIPEntityException:
            receivedConnectedSIPMessage.disconnect()
        except SendResponseSIPEntityException as ex:
            self.sendErrorResponseForResponse(receivedConnectedSIPMessage, statusCodeInteger=ex.statusCode, reasonPhraseString=ex.reasonPhrase, descriptionString=ex.description)

    def transportConnectionIDForRequest(self, receivedConnectedSIPMessage):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.1
        In some circumstances, a proxy MAY forward requests using stateful
       transports (such as TCP) without being transaction-stateful.  For
       instance, a proxy MAY forward a request from one TCP connection to
       another transaction statelessly as long as it places enough
       information in the message to be able to forward the response down
       the same connection the request arrived on.
        '''
        return receivedConnectedSIPMessage.connection.id

    def validateRequest(self, receivedConnectedSIPMessage):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.3
        Validate the request
             - isMalformed is False
             - Check for a merged request (i.e. 482 (Loop Detected))
             - Check the request URI scheme, to ensure that we understand it (i.e. "sip" or "sips") 416 (Unsupported URI Scheme)
             - Check Max-Forwards.  If 0, don't forward the request, 483 (Too Many Hops)
             - (optional) Loop check.  Via header with sent-by value that's already been placed into previous requests by us
                - Maybe only appropriate for stateful proxy.
             - Proxy-Require test - 420 (Bad Extension)
             - Proxy-Authorization check -
        '''
        sipMessage = receivedConnectedSIPMessage.sipMessage
        if sipMessage.isMalformed:
            # TODO - do we need to drop the connection if malformed?  What does the RFC say about that?
            raise DropMessageSIPEntityException(descriptionString='Received SIP message was malformed.')
        # TODO - we instantiate a first-class SIPURI object here.  We probably want to do that in the start line object instead.
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        if requestURI.scheme not in ['sip', 'sips']:
            raise SendResponseSIPEntityException(statusCodeInteger=416, reasonPhraseString='Unsupported URI Scheme')
        if sipMessage.maxForwards is not None:
            if sipMessage.maxForwards <= 0:
                raise SendResponseSIPEntityException(statusCodeInteger=483, reasonPhraseString='Too many hops')
        # TODO - for now, skip the optional loop detection.
        # TODO - for now, skip the Proxy-Require header field check.
        #    We will flesh out Proxy-Require once we know for sure which features we handle.
        # TODO - for now, we don't do authentication.  When we do, the authorization check will be here.
        # TODO - "If any of these checks fail, the element MUST behave as a user agent server (see Section 8.2) and respond with an error code."

    def createConnectedSIPMessageToSendForRequest(self, receivedConnectedSIPMessage):
        # We do a total copy of the sipMessage.  The connection will be replaced later.
        sipMessage = receivedConnectedSIPMessage.sipMessage.__class__.newParsedFrom(receivedConnectedSIPMessage.rawString)
        return ConnectedSIPMessage(receivedConnectedSIPMessage.connection, sipMessage)

    def preprocessRoutingInformationForRequest(self, connectedSIPMessageToSend):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.4

        '''
        # TODO - for now, skip strict route stuff in the first paragraph of 16.4
        sipMessage = connectedSIPMessageToSend.sipMessage
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        maddr = requestURI.parameterNamed('maddr')
        if maddr:
            # TODO - for now, skip the maddr processing step.
            pass
        routeURIs = sipMessage.routeURIs
        if routeURIs:
            if self.sipURIMatchesUs(routeURIs[0]):
                # TODO - remove first route header, because it matches us.
                # TODO - need to test that removeFirstHeaderFieldOfClass() works correctly.  Header field tests should be written for that.
                sipMessage.removeFirstHeaderFieldOfClass(RouteSIPHeaderField)

    def determineTargetForRequest(self, connectedSIPMessageToSend):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.5
        Special consideration for stateless proxies explained in section 16.11
        - Choose only one target (not forking), based on time-invariant stuff.
        '''
        sipMessage = connectedSIPMessageToSend.sipMessage
        requestURI = SIPURI.newParsedFrom(sipMessage.requestURI)
        maddr = requestURI.parameterNamed('maddr')
        if maddr:
            return requestURI
        if not self.sipURIMatchesUs(requestURI):
            return requestURI
        # TODO - we are responsible for this request.  We will have a registrar
        # or location service, probably implemented using the Strategy pattern,
        # but for now, let's just make a degenerate behavior, by answering a 404.  We will
        # implement that location service later.  Also allow other developers to write their
        # own Strategy objects.
        raise SendResponseSIPEntityException(statusCodeInteger=404, reasonPhraseString='Not Found')


    def forwardRequestToTarget(self, connectedSIPMessageToSend, targetURI=None, transportIDForVia=None):
        '''
        https://tools.ietf.org/html/rfc3261#section-16.6
        Special consideration for stateless proxies explained in section 16.11
        - The unique branch id must be invariant for requests with identical headers.
        - Item 10 will send the forwarded message directly to a transportConnection, not transaction.
        '''
        sipMessage = connectedSIPMessageToSend.sipMessage
        # TODO: in progress
        # 1. Copy request
        #   (already copied it)
        # 2.  Update the Request-URI
        # TODO: need to remove any URI parameters that are not allowed in a Request URI.
        # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
        if targetURI:
            sipMessage.startLine.requestURI = targetURI
        # 3.  Update the Max-Forwards header field
        if sipMessage.maxForwards is not None:
            # TODO:  When you use -= 1 on an integer sip header field's integerValue parameter, does that work?  Need to write a test.
            sipMessage.header.maxForwardsHeaderField.integerValue -= 1
        else:
            # TODO: inserting a header field - we should make a method that inserts it using an aesthetically-pleasing order
            # relative to other header fields.  Each header field concrete subclass would have an integer sort attribute for that.
            sipMessage.header.addHeaderField(MaxForwardsSIPHeaderField.newForIntegerValue(70))
        # 4.  Optionally add a Record-route header field value
        # TODO: is this the best way to get the URI host?
        # Are record-route header fields only used for INVITE?  Should we only do this if it's an INVITE?
        #    Answer:  No.  See RFC3261 16.6  point 4
        # TODO: sip or sips scheme?  Should that be derived from the transportConnection?  For now, hard-code to 'sip'
        recordRouteURI = SIPURI.newForAttributes(host=self.transports[0].bindAddress, port=self.transports[0].bindPort, scheme='sip', parameterNamesAndValueStrings={'lr': None})
        recordRouteHeaderField = RecordRouteSIPHeaderField.newForAttributes(recordRouteURI)
        if transportIDForVia:
            # Do we want to put that state into this header or the Via?
            #    Answer:  we want it here.  See RFC3261 16.6  point 4
            recordRouteHeaderField.parameterNamedPut('bobstackTransportID', transportIDForVia)
        sipMessage.header.addHeaderFieldBeforeHeaderFieldsOfSameClass(recordRouteHeaderField)

        # 5.  Optionally add additional header fields
        # TODO: make the server header field a user-settable parameter.
        sipMessage.header.addHeaderField(ServerSIPHeaderField.newForValueString('BobStack'))

        # 6.  Postprocess routing information
        routeURIs = sipMessage.header.routeURIs
        if routeURIs:
            if 'lr' not in routeURIs[0].parameterNames:
                # TODO: When we set an attribute on the start line, we may need to manually mark the sip message as dirty.
                sipMessage.header.addHeaderFieldAfterHeaderFieldsOfSameClass(RouteSIPHeaderField.newForAttributes(SIPURI.newParsedFrom(sipMessage.startLine.requestURI)))
                sipMessage.startLine.requestURI = routeURIs[0].rawString
                # TODO: Is the class actually the same object, considering that we're accessing it from a different directory?  Trap for young players.
                sipMessage.header.removeFirstHeaderFieldOfClass(RouteSIPHeaderField)
                uriToDetermineNextHop = sipMessage.requestURI
            else:
                uriToDetermineNextHop = routeURIs[0]
        else:
            uriToDetermineNextHop = sipMessage.requestURI

        # 7.  Determine the next-hop address, port, and transport
        nextHopConnectedTransportConnection = self.connectedTransportConnectionForSIPURI(uriToDetermineNextHop)
        if not nextHopConnectedTransportConnection:
            # TODO:  we could not connect to the next-hop.  Return some error code.  Which error code and reason phrase?  400 and could not connect are NOT correct.
            raise SendResponseSIPEntityException(statusCodeInteger=400, reasonPhraseString='Could not connect')

        # 8.  Add a Via header field value
        # TODO:  For now, don't do the loop / spiral detection stuff.
        sipMessage.header.addHeaderFieldBeforeHeaderFieldsOfSameClass(self.newViaHeaderFieldForSIPMessage(sipMessage))

        # 9.  Add a Content-Length header field if necessary
        # TODO: if the target transport is stream-oriented, e.g. TLS or TCP, and the message has no Content-Length: header field, add one.
        # TODO: So we'll need to wait until step 7 is done, to know the transport.
        if not sipMessage.header.contentLengthHeaderField:
            if nextHopConnectedTransportConnection.isStateful:
                # TODO: if the target transport is stream-oriented, e.g. TLS or TCP, and the message has no Content-Length: header field, add one.
                sipMessage.header.addHeaderField(self.newContentLengthHeaderFieldForSIPMessage(sipMessage))

        # 10. Forward the new request
        # TODO:  exception handling?
        nextHopConnectedTransportConnection.sendMessage(sipMessage)

        # 11. Set timer C - not applicable for stateless.  Huzzah!

    def connectedTransportConnectionForSIPURI(self, aSIPURI):
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
        nextHopAddress = aSIPURI.host
        nextHopPort = aSIPURI.derivedPort
        # TODO:  Not yet done.  We will return an existing protocol that matches the uri's host, port, and is appropriate
        # for the uri's scheme.  If it doesn't exist, we will create a new one and connect it.  If connection fails, we will
        # return None.
        # TODO:  THIS IS NEXT!
        answer = None
        return answer


    def newViaHeaderFieldForSIPMessage(self, aSIPMessage):
        # TODO:  WE NEED TO USE THE TARGET SET ATTRIBUTES!  SEE "7." ABOVE!
        # TODO:  Need to do transport string as well.
        answer = ViaSIPHeaderField.newForAttributes()
        answer.host = self.ourHost
        answer.port = self.ourPort
        answer.generateInvariantBranchForSIPHeader(aSIPMessage.header)
        return answer

    def newContentLengthHeaderFieldForSIPMessage(self, aSIPMessage):
        return ContentLengthSIPHeaderField.newForIntegerValue(len(aSIPMessage.body))

    @property
    def ourHost(self):
        # TODO: This is very simplistic for now.
        try:
            return self.homeDomains[0]
        except IndexError:
            return '127.0.0.1'

    def ourPort(self):
        # TODO: This is very simplistic for now.
        try:
            return self.transports[0].bindPort
        except IndexError:
            return 5060

    def sipURIMatchesUs(self, aSIPURI):
        # TODO - we will also need to verify match of transport protocol and port, right?
        return aSIPURI.host in self.homeDomains

    def sendErrorResponseForRequest(self, receivedConnectedSIPMessage, statusCodeInteger=500, reasonPhraseString='Server Error', descriptionString='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # TODO: I am not confident that we are creating all necessary header fields, but I don't
        # see RFC documentation of all that needs to be there.  Look harder.  There is plenty in
        # section 16.7 about forwarding responses, but not creating responses.
        sipRequestReplyingTo = receivedConnectedSIPMessage.sipMessage
        connection = receivedConnectedSIPMessage.connection
        sipResponse = SIPResponse.newForAttributes(statusCode=statusCodeInteger, reasonPhrase=reasonPhraseString)
        sipResponse.header.addHeaderField(sipRequestReplyingTo.header.toHeaderField)
        sipResponse.header.addHeaderField(sipRequestReplyingTo.header.fromHeaderField)
        sipResponse.header.addHeaderField(ContentLengthSIPHeaderField.newForIntegerValue(0))
        connection.sendMessage(sipResponse)

    def transportConnectionIDForResponse(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def responseSendTransportConnectionForConnectionID(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def validateResponse(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def responseShouldBeForwarded(self, receivedConnectedSIPMessage):
        # TODO
        pass

    def createConnectedSIPMessageToSendForResponse(self, receivedConnectedSIPMessage, responseSendTransportConnection):
        # TODO
        pass

    def removeViaForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def rewriteRecordRouteForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def determineTargetForResponse(self, connectedSIPMessageToSend):
        # TODO
        pass

    def forwardResponseToTarget(self, connectedSIPMessageToSend, targetURI=None):
        # TODO
        pass

    def sendErrorResponseForResponse(self, receivedConnectedSIPMessage, statusCodeInteger=500, reasonPhraseString='Server Error', descriptionString='An unknown server error occurred.'):
        # TODO: I believe we need to reliably send this response, including retransmission, etc.  For now, just send the damn thing.
        # TODO
        pass

