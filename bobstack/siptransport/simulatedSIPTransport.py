from sipTransport import SIPTransport
from simulatedSIPTransportConnection import SimulatedSIPTransportConnection
from simulatedNetwork import SimulatedNetwork


class SimulatedSIPTransport(SIPTransport):
    @property
    def transport_parameter_name(self):
        return 'SIM'

    def connect_to_address_and_port(self, address_string, port_integer):
        # TODO: need to make (and test) exception handlers, not just events.
        connected_transport = SimulatedNetwork.instance.bound_transport_with_address_and_port(address_string, port_integer)
        if connected_transport:
            if connected_transport is not self:
                answer = self.basic_connect_to_address_and_port(address_string, port_integer)
                connected_transport.basic_connect_to_address_and_port(self.bind_address, self.bind_port)
                return answer
            else:
                self.trigger_could_not_make_connection(address_string, port_integer)
        else:
            self.trigger_could_not_make_connection(address_string, port_integer)

    def basic_connect_to_address_and_port(self, address_string, port_integer):
        # TODO: the local port is not necessarily our bind port, it may be a random upper port.
        connection = SimulatedSIPTransportConnection(self.bind_address, address_string, self.bind_port, port_integer)
        self.connections.append(connection)
        self.subscribe_to_transport_connection_events(connection)
        self.trigger_made_connection(connection)
        return connection

    def bind(self):
        if SimulatedNetwork.instance.bind_transport(self):
            self.trigger_bound()
        else:
            self.trigger_bind_failed()
