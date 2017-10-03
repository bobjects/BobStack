#!/usr/bin/env python2
import glob
import sys

import dpkt

sys.path.append("../bobstack")
# from sipmessaging.sipMessageFactory import SIPMessageFactory
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from bobstack.sipmessaging import SIPMessageFactory
import os
import re
import timeit
import bobstack.tests_slow.testlogfilelocations

# interimFile1PathName = '../proprietary-test-data/sanitized/interim1.txt'
# interimFile2PathName = '../proprietary-test-data/sanitized/interim2.txt'
# sanitizedFilePathName = '../proprietary-test-data/sanitized/sanitized.txt'
messageSeparator = "__MESSAGESEPARATOR__"
rawFileMessageSeparatorRegexes = [ "^>>>>>>>>>>  [^>]*>>>>>>>>>>>",
                                   "^>>>>>>>>>>  [^>]*>>>>>>>>>>",  # for some reason, this is not catching 8 lines.
                                   "^<<<<<<<<<<  [^<]*<<<<<<<<<<",  # for some reason, this is not catching 32 lines.
                                   "^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* [^\*]*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*",
                                   "^##################################### [^#]*##########################" ]
rawFileMessageSeparatorRegexes = [re.compile(s) for s in rawFileMessageSeparatorRegexes]
sanitizedMessageSeparatorRegex = re.compile("^__MESSAGESEPARATOR__")
startLineRegexes = ["^SIP/2.0\s+([\d]+)+\s+(.+)\s*$", "^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$"]
startLineRegexes = [re.compile(s) for s in startLineRegexes]



def createInterim1File():
    try:
        with open(interimFile1PathName, "w") as interimFile1:
            print("creating interim file 1")
            for rawLogFileDirectoryPathName in rawLogFileDirectoryPathNames:
                # for rawLogFilePathName in os.listdir(rawLogFileDirectoryPathName):
                for rawLogFilePathName in sorted(glob.iglob(rawLogFileDirectoryPathName + '/tlslog*.txt')):
                    print(rawLogFilePathName)
                    with open(rawLogFilePathName, "r") as rawLogFile:
                        for line in rawLogFile:
                            line = line.replace("\r\r\n", "\r\n")
                            if any(regex.match(line) for regex in rawFileMessageSeparatorRegexes):
                                line = messageSeparator + "\r\n"
                            interimFile1.write(line)
                        interimFile1.write("\r\n")
    except IOError:
        print('WARNING:  could not create interim file named {0}'.format(interimFile1PathName))


def createInterim2File():
    try:
        with open(interimFile1PathName, "r") as interimFile1:
            print("creating interim file 2")
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
                print(str(totalSIPMessages) + " total SIP messages")
    except IOError:
        print('WARNING:  could not create interim file named {0}'.format(interimFile1PathName))


def processInterimFile():
    try:
        with open(sanitizedFilePathName, "w") as sanitizedFile:
            print("processing interim file 2")
            with open(interimFile2PathName, "r") as interimFile2:
                currentlyInMessage = False
                currentMessageString = ''
                totalSIPMessages = 0
                for line in interimFile2:
                    if currentlyInMessage:
                        if sanitizedMessageSeparatorRegex.match(line):
                            # some messages are two bytes too long, because of weirdness in our logging code!
                            # No real way to figure out which
                            # ones, except by instantiating a SIPMessage and checking.  Look for messages
                            # that are exactly two bytes too long, and chop them down.
                            sip_message = SIPMessageFactory().next_for_string(currentMessageString)
                            truncateBytes = sip_message.content.__len__() - sip_message.header.content_length
                            if truncateBytes == 2:
                                currentMessageString = currentMessageString[:currentMessageString.__len__() - 2]

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
                print(str(totalSIPMessages) + " total SIP messages")
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


def deleteInterimFiles():
    try:
        os.remove(interimFile1PathName)
        os.remove(interimFile2PathName)
    except OSError:
        pass

# @profile
def processPCAPFiles():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing pcap files")
            for pcapDirectoryPathName in pcapDirectoryPathNames:
                for pcapFilePathName in sorted(glob.iglob(pcapDirectoryPathName + '/*.pcap')):
                    print(pcapFilePathName)
                    with open(pcapFilePathName, "r") as pcapFile:
                        for ts, pkt in dpkt.pcap.Reader(pcapFile):
                            eth = dpkt.ethernet.Ethernet(pkt)
                            if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
                                continue
                            ip = eth.data
                            if (ip.p==dpkt.ip.IP_PROTO_UDP or ip.p==dpkt.ip.IP_PROTO_TCP) and ip.data.dport in [5060, 5062, 5080]:
                                data = ip.data.data
                                if data.__len__() > 2:
                                    if re.match('[^\s]+', data):  # Bria and some others periodically send CRLFCRLF by itself, presumably as a keepalive.  We don't want those.
                                        sanitizedFile.write(data)
                                        sanitizedFile.write(messageSeparator + "\r\n")
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


# @profile
def processFreeswitchFiles():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing Freeswitch files")
            for freeswitchDirectoryPathName in freeswitchDirectoryPathNames:
                for freeswitchFilePathName in sorted(glob.iglob(freeswitchDirectoryPathName + '/*')):
                    print(freeswitchFilePathName)
                    with open(freeswitchFilePathName, "r") as freeswitchFile:
                        stringio = StringIO()
                        state = 'outsideOfMessage'
                        lineNumber = 0
                        for line in freeswitchFile:
                            lineNumber += 1
                            if state == 'outsideOfMessage':
                                if re.match('^send \d+ bytes to', line) or re.match('^recv \d+ bytes from', line):
                                    state = 'waitingForFirstDashes'
                            elif state == 'waitingForFirstDashes':
                                if re.match('^   ---------------', line):
                                    stringio = StringIO()
                                    state = 'inMessage'
                                else:
                                    print('ERROR!  Line {0} - First dashes not found.'.format(lineNumber))
                                    stringio.close()
                                    state = 'outsideOfMessage'
                            elif state == 'inMessage':
                                if re.match('^   ---------------', line):
                                    sanitizedFile.write(stringio.getvalue())
                                    sanitizedFile.write(messageSeparator + "\r\n")
                                    stringio.close()
                                    state = 'outsideOfMessage'
                                else:
                                    if not re.match('^   ', line):
                                        print('WARNING!  Line {0} - In message, but line is not preceeded by 3 spaces.  Rejecting message.'.format(lineNumber))
                                        stringio.close()
                                        state = 'outsideOfMessage'
                                    else:
                                        stringio.write(line[3:].replace('\n', '\r\n'))
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))

def runAll():
    createInterim1File()
    createInterim2File()
    processInterimFile()
    deleteInterimFiles()
    processPCAPFiles()
    processFreeswitchFiles()

if __name__ == '__main__':
    for logFileDict in bobstack.tests_slow.testlogfilelocations.logFileDicts:
        # rawLogFileDirectoryPathNames = [ '../proprietary-test-data/big-lab-test-logs-raw',
        #                                  '../proprietary-test-data/cust-1-logs-raw',
        #                                  '../proprietary-test-data/cust-3-logs-raw' ]

        # rawLogFileDirectoryPathNames = []
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cloud',
        #                            '../proprietary-test-data/big-lab-test-logs-pcap',
        #                            '../proprietary-test-data/client-lab-test-logs-pcap',
        #                            '../proprietary-test-data/cust-2-logs-pcap',
        #                            '../proprietary-test-data/cust-4-logs-pcap',
        #                            '../proprietary-test-data/from-bobstack-testbed' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cloud' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cust-2-logs-pcap' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/from-bobstack-testbed' ]
        rawLogFileDirectoryPathNames = logFileDict['rawLogFileDirectoryPathNames']
        pcapDirectoryPathNames = logFileDict['pcapDirectoryPathNames']
        freeswitchDirectoryPathNames = logFileDict['freeswitchDirectoryPathNames']
        interimFile1PathName = logFileDict['interimFile1PathName']
        interimFile2PathName = logFileDict['interimFile2PathName']
        sanitizedFilePathName = logFileDict['sanitizedFilePathName']

        # print timeit.timeit(createInterim1File, number=1)
        # print timeit.timeit(createInterim2File, number=1)
        # print timeit.timeit(processInterimFile, number=1)
        # deleteInterimFiles()
        # print timeit.timeit(processPCAPFiles, number=1)
        print(timeit.timeit(runAll, number=1))
