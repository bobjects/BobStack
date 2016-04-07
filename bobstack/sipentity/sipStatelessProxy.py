from sipEntity import SIPEntity


class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the request.  Add headers, forward it downstream, etc.
        # - If the transport connection isStateful, get the ID of the transport, and use it ensure that
        #   our response goes back through the correct transport connection.
        # - Validate the request - https://tools.ietf.org/html/rfc3261#section-16.3
        #     - isMalformed is False
        #     - Check for a merged request (i.e. 482 (Loop Detected))
        #     - Check the request URI scheme, to ensure that we understand it (i.e. "sip" or "sips") 416 (Unsupported URI Scheme)
        #     - Check Max-Forwards.  If 0, don't forward the request, 483 (Too Many Hops)
        #     - (optional) Loop check.  Via header with sent-by value that's already been placed into previous requests by us
        #        - Maybe only appropriate for stateful proxy.
        #     - Proxy-Require test - 420 (Bad Extension)
        #     - Proxy-Authorization check - 
        print "Stateless proxy request payload - " + str(aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the response.  Remove headers, forward it upstream, etc.
        print "Stateless proxy response payload - " + str(aConnectedSIPMessage)

