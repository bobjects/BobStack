try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from collections import OrderedDict
from sipHeaderFieldFactory import SIPHeaderFieldFactory


class SIPHeader(object):
    @classmethod
    def newParsedFrom(cls, stringioToParse):
        answer = cls()
        answer.parseAttributesFromStringIO(stringioToParse)
        return answer

    @classmethod
    def newForAttributes(cls, headerFields=None):
        answer = cls()
        if not headerFields:
            answer.headerFields = []
        else:
            answer.headerFields = headerFields
        return answer

    def __init__(self):
        self._headerFields = []
        self._knownHeaderFields = None
        self._unknownHeaderFields = None
        self._contentLengthHeaderField = None

    def parseAttributesFromStringIO(self, stringioToParse):
        self._headerFields = SIPHeaderFieldFactory().allForStringIO(stringioToParse)

    def renderRawStringFromAttributes(self, stringio):
        for headerField in self.headerFields:
            stringio.write(headerField.rawString)
            stringio.write("\r\n")
        stringio.write("\r\n")

    @property
    def contentLength(self):
        if self.contentLengthHeaderField is not None:
            return self.contentLengthHeaderField.value
        return 0

    @property
    def contentLengthHeaderField(self):
        if not self._contentLengthHeaderField:
            self._contentLengthHeaderField = next((headerField for headerField in self.headerFields if headerField.isContentLength), None)
        return self._contentLengthHeaderField

    @property
    def knownHeaderFields(self):
        if not self._knownHeaderFields:
            self._knownHeaderFields = [headerField for headerField in self.headerFields if headerField.isKnown]
        return self._knownHeaderFields

    @property
    def unknownHeaderFields(self):
        if not self._unknownHeaderFields:
            self._unknownHeaderFields = [headerField for headerField in self.headerFields if headerField.isUnknown]
        return self._unknownHeaderFields

    @property
    def isValid(self):
        return all(f.isValid for f in self.headerFields)

    @property
    def headerFields(self):
        return self._headerFields

    @headerFields.setter
    def headerFields(self, aCollection):
        # TODO:  work in progress
        # TODO:  NOTE:  WE CANNOT USE DICT OR ORDEREDDICT, BECAUSE WE NEED TO HAVE MULTIPLE HEADERS WITH SAME FIELD NAMES.
        # TODO:  INSTEAD, USE LIST OF TUPLES OR LIST OF LISTS

        if aCollection.__class__ == list:
            self._headerFields = aCollection
        elif aCollection.__class__ == dict:
            # TODO
            pass
        elif aCollection.__class__ == OrderedDict:
            # TODO
            pass
        else:
            raise(ValueError, "headerFields must be a list, dict, or OrderedDictionary")

