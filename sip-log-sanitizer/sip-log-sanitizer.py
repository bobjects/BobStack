#!/usr/bin/python
import sys
sys.path.append("../bobstack")
from sipmessaging.sipMessageFactory import SIPMessageFactory
import os
import re
import timeit

# interimFile1PathName = '/tmp/interim1.txt'
# interimFile2PathName = '/tmp/interim2.txt'
interimFile1PathName = '../proprietary-test-data/ft-huachuca-test-logs-sanitized/interim1.txt'
interimFile2PathName = '../proprietary-test-data/ft-huachuca-test-logs-sanitized/interim2.txt'
sanitizedFilePathName = '../proprietary-test-data/ft-huachuca-test-logs-sanitized/sanitized.txt'
rawLogFileDirectoryPathNames = [ '../proprietary-test-data/ft-huachuca-test-logs-raw', '../proprietary-test-data/vance-logs-raw' ]
messageSeparator = "__MESSAGESEPARATOR__"
rawFileMessageSeparatorRegexes = [ "^>>>>>>>>>>  [^>]*>>>>>>>>>>>",
                                   "^>>>>>>>>>>  [^>]*>>>>>>>>>>", # for some reason, this is not catching 8 lines.
                                   "^<<<<<<<<<<  [^<]*<<<<<<<<<<", # for some reason, this is not catching 32 lines.
                                   "^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* [^\*]*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*",
                                   "^##################################### [^#]*##########################" ]
rawFileMessageSeparatorRegexes = [re.compile(s) for s in rawFileMessageSeparatorRegexes]
sanitizedMessageSeparatorRegex = re.compile("^__MESSAGESEPARATOR__")
startLineRegexes = ["^SIP/2.0\s+([\d]+)+\s+(.+)\s*$", "^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$"]
startLineRegexes = [re.compile(s) for s in startLineRegexes]

def createInterim1File():
    print "creating interim file 1"
    with open(interimFile1PathName, "w") as interimFile1:
        for rawLogFileDirectoryPathName in rawLogFileDirectoryPathNames:
            for rawLogFilePathName in os.listdir(rawLogFileDirectoryPathName):
                print rawLogFilePathName
                with open(rawLogFileDirectoryPathName + "/" + rawLogFilePathName, "r") as rawLogFile:
                    for line in rawLogFile:
                        line = line.replace("\r\r\n", "\r\n")
                        if any(regex.match(line) for regex in rawFileMessageSeparatorRegexes):
                            line = messageSeparator + "\r\n"
                        interimFile1.write(line)
                    interimFile1.write("\r\n")

def createInterim2File():
    print "creating interim file 2"
    with open(interimFile1PathName, "r") as interimFile1:
        with open(interimFile2PathName, "w") as interimFile2:
            currentlyInMessage = False
            totalSIPMessages = 0
            for line in interimFile1:
                if currentlyInMessage:
                    if sanitizedMessageSeparatorRegex.match(line):
                        interimFile2.write(line)
                        currentlyInMessage = False
                    else:
                        interimFile2.write(line)
                else:
                    if any(regex.match(line) for regex in startLineRegexes):
                        # print "."
                        totalSIPMessages += 1
                        currentlyInMessage = True
                        interimFile2.write(line)
            print str(totalSIPMessages) + " total SIP messages"

def processInterimFile():
    print "processing interim file 2"
    with open(sanitizedFilePathName, "w") as sanitizedFile:
        with open(interimFile1PathName, "r") as interimFile1:
            currentlyInMessage = False
            currentMessageString = ''
            totalSIPMessages = 0
            for line in interimFile1:
                if currentlyInMessage:
                    if sanitizedMessageSeparatorRegex.match(line):
                        # some messages are two bytes too long, because of weirdness in our logging code!
                        # No real way to figure out which
                        # ones, except by instantiating a SIPMessage and checking.  Look for messages
                        # that are exactly two bytes too long, and chop them down.
                        sipMessage = SIPMessageFactory().nextForString(currentMessageString)
                        truncateBytes = sipMessage.content.__len__() - sipMessage.header.contentLength
                        if truncateBytes == 2:
                            currentMessageString = currentMessageString[:currentMessageString.__len__()-2]

                        sanitizedFile.write(currentMessageString)
                        sanitizedFile.write(line)
                        currentlyInMessage = False
                    else:
                        currentMessageString += line
                else:
                    if any(regex.match(line) for regex in startLineRegexes):
                        # print "."
                        totalSIPMessages += 1
                        currentlyInMessage = True
                        currentMessageString = ''
                        sanitizedFile.write(line)
            print str(totalSIPMessages) + " total SIP messages"


if __name__ == '__main__':
    print timeit.timeit(createInterim1File, number=1)
    print timeit.timeit(createInterim2File, number=1)
    print timeit.timeit(processInterimFile, number=1)
