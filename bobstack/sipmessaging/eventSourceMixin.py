from inspect import getargspec


class EventSourceMixin(object):
    def __init__(self):
        self.eventsAndObservingMethods = {}

    def when_event_do(self, event_name, observing_method):
        if event_name not in self.eventsAndObservingMethods:
            self.eventsAndObservingMethods[event_name] = []
        self.eventsAndObservingMethods[event_name].append(observing_method)

    def when_event_do_not(self, event_name, observing_method):
        if event_name in self.eventsAndObservingMethods:
            if observing_method in self.eventsAndObservingMethods[event_name]:
                self.eventsAndObservingMethods[event_name].remove(observing_method)

    def trigger_event(self, event_name, object_to_pass=None):
        if event_name in self.eventsAndObservingMethods:
            for observing_method in self.eventsAndObservingMethods[event_name]:
                # TODO:  This is shitty.  Make it less shitty.  De-shittify it.
                if getargspec(observing_method).args.__len__() == 2:
                    observing_method(object_to_pass)
                else:
                    observing_method()
