try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from sipHeaderFieldFactory import SIPHeaderFieldFactory

class SIPHeader(object):
    def __init__(self, stringioToParse=None, headerFields=None):
        # on the off chance that stringioToParse and the other parameters are all specified,
        # ignore the other parameters, and populate our attributes by parsing.
        if not stringioToParse:
            if headerFields:
                self.headerFields = headerFields
            else:
                self.headerFields = []
        else:
            self.parseAttributesFromStringIO(stringioToParse)

    def parseAttributesFromStringIO(self, stringioToParse):
        self.headerFields = SIPHeaderFieldFactory().allForStringIO(stringioToParse)

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

    # TODO:  Need to cache.  Look into @cache decorator.
    @property
    def contentLengthHeaderField(self):
        return next(headerField for headerField in self.headerFields if headerField.isContentLength)

    # TODO:  Need to cache.  Look into @cache decorator.
    @property
    def unknownHeaderFields(self):
        return [headerField for headerField in self.headerFields if headerField.isUnknown]