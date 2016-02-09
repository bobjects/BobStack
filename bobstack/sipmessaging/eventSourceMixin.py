from inspect import getargspec


class EventSourceMixin(object):
    def __init__(self):
        self.eventsAndObservingMethods = {}

    def whenEventDo(self, eventName, observingMethod):
        if eventName not in self.eventsAndObservingMethods:
            self.eventsAndObservingMethods[eventName] = []
        self.eventsAndObservingMethods[eventName].append(observingMethod)

    def whenEventDoNot(self, eventName, observingMethod):
        if eventName in self.eventsAndObservingMethods:
            if observingMethod in self.eventsAndObservingMethods[eventName]:
                self.eventsAndObservingMethods[eventName].remove(observingMethod)

    def triggerEvent(self, eventName, objectToPass=None):
        if eventName in self.eventsAndObservingMethods:
            for observingMethod in self.eventsAndObservingMethods[eventName]:
                # TODO:  This is shitty.  Make it less shitty.  De-shittify it.
                if getargspec(observingMethod).args.__len__() == 2:
                    observingMethod(objectToPass)
                else:
                    observingMethod()
