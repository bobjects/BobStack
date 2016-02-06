#!/usr/bin/python
import os
import re
import timeit

# interimFile1PathName = '/tmp/interim1.txt'
# interimFile2PathName = '/tmp/interim2.txt'
interimFile1PathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-sanitized/interim1.txt'
interimFile2PathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-sanitized/interim2.txt'
sanitizedFilePathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-sanitized/sanitized.txt'
rawLogFileDirectoryPathNames = [ '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-raw', '/Users/bob/bobstack/proprietary-test-data/vance-logs-raw' ]
messageSeparator = "__MESSAGESEPARATOR__"
rawFileMessageSeparatorRegexes = [ "^>>>>>>>>>>  [^>]*>>>>>>>>>>>",
                                   "^>>>>>>>>>>  [^>]*>>>>>>>>>>",
                                   "^<<<<<<<<<<  [^>]*<<<<<<<<<<",
                                   "^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* [^\*]*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*",
                                   "^##################################### [^#]*##########################" ]
rawFileMessageSeparatorRegexes = [re.compile(s) for s in rawFileMessageSeparatorRegexes]
sanitizedMessageSeparatorRegex = re.compile("^__MESSAGESEPARATOR__")
startLineRegexes = ["^SIP/2.0\s+([\d]+)+\s+(.+)\s*$", "^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$"]
# startLineRegexes = ["^([^\s]+)\s+([^\s]+)\s+SIP/2.0$"]
#startLineRegexes = ["^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$"]
startLineRegexes = [re.compile(s) for s in startLineRegexes]

def createInterimFile():
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

def processInterimFile():
    with open(sanitizedFilePathName, "w") as sanitizedFile:
        with open(interimFile1PathName, "r") as interimFile1:
            currentlyInMessage = False
            totalSIPMessages = 0
            for line in interimFile1:
                if currentlyInMessage:
                    if sanitizedMessageSeparatorRegex.match(line):
                        sanitizedFile.write(line)
                        currentlyInMessage = False
                    else:
                        sanitizedFile.write(line)
                else:
                    if any(regex.match(line) for regex in startLineRegexes):
                        # print "."
                        totalSIPMessages += 1
                        currentlyInMessage = True
                        sanitizedFile.write(line)
            print str(totalSIPMessages) + " total SIP messages"


if __name__ == '__main__':
    print timeit.timeit(createInterimFile, number=1)
    print timeit.timeit(processInterimFile, number=1)
