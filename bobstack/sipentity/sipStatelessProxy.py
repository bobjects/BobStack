from sipEntity import SIPEntity


class SIPStatelessProxy(SIPEntity):
    def __init__(self):
        super(SIPStatelessProxy, self).__init__()

    def receivedValidConnectedRequestEventHandler(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the request.  Add headers, forward it downstream, etc.
        # - If the transport connection isStateful, get the ID of the transport, and use it ensure that
        #   our response goes back through the correct transport connection.
        print "Stateless proxy request payload - " + str(aConnectedSIPMessage)

    def receivedValidConnectedResponseEventHandler(self, aConnectedSIPMessage):
        # TODO - do a lot of cool stuff with the response.  Remove headers, forward it upstream, etc.
        print "Stateless proxy response payload - " + str(aConnectedSIPMessage)

