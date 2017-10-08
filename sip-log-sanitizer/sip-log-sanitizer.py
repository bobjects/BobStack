#!/usr/bin/env python2
import glob
import sys
import dpkt
import os
import re
import timeit
sys.path.append("../../..")
from bobstack.sipmessaging import SIPMessageFactory
import bobstack.tests_slow.testlogfilelocations
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

# interim_file_1PathName = '../proprietary-test-data/sanitized/interim1.txt'
# interim_file_2PathName = '../proprietary-test-data/sanitized/interim2.txt'
# sanitizedFilePathName = '../proprietary-test-data/sanitized/sanitized.txt'
message_separator = "__MESSAGESEPARATOR__"
raw_file_message_separator_regexes = ["^>>>>>>>>>>  [^>]*>>>>>>>>>>>",
                                      "^>>>>>>>>>>  [^>]*>>>>>>>>>>",  # for some reason, this is not catching 8 lines.
                                      "^<<<<<<<<<<  [^<]*<<<<<<<<<<",  # for some reason, this is not catching 32 lines.
                                      "^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* [^\*]*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*",
                                      "^##################################### [^#]*##########################"]
raw_file_message_separator_regexes = [re.compile(s) for s in raw_file_message_separator_regexes]
sanitized_message_separator_regex = re.compile("^__message_separator__")
start_line_regexes = ["^SIP/2.0\s+([\d]+)+\s+(.+)\s*$", "^([^\s]+)\s+([^\s]+)\s+SIP/2.0\s*$"]
start_line_regexes = [re.compile(s) for s in start_line_regexes]


def create_interim_1_file():
    try:
        with open(interim_file_1PathName, "w") as interim_file_1:
            print("creating interim file 1")
            for raw_log_file_directory_path_name in raw_log_file_directory_path_names:
                # for raw_log_file_path_name in os.listdir(raw_log_file_directory_path_name):
                for raw_log_file_path_name in sorted(glob.iglob(raw_log_file_directory_path_name + '/tlslog*.txt')):
                    print(raw_log_file_path_name)
                    with open(raw_log_file_path_name, "r") as raw_log_file:
                        for line in raw_log_file:
                            line = line.replace("\r\r\n", "\r\n")
                            if any(regex.match(line) for regex in raw_file_message_separator_regexes):
                                line = message_separator + "\r\n"
                            interim_file_1.write(line)
                        interim_file_1.write("\r\n")
    except IOError:
        print('WARNING:  could not create interim file named {0}'.format(interim_file_1PathName))


def create_interim_2_file():
    try:
        with open(interim_file_1PathName, "r") as interim_file_1:
            print("creating interim file 2")
            with open(interim_file_2PathName, "w") as interim_file_2:
                currently_in_message = False
                total_sip_messages = 0
                for line in interim_file_1:
                    if currently_in_message:
                        if sanitized_message_separator_regex.match(line):
                            interim_file_2.write(line)
                            currently_in_message = False
                        else:
                            interim_file_2.write(line)
                    else:
                        if any(regex.match(line) for regex in start_line_regexes):
                            # print "."
                            total_sip_messages += 1
                            currently_in_message = True
                            interim_file_2.write(line)
                print(str(total_sip_messages) + " total SIP messages")
    except IOError:
        print('WARNING:  could not create interim file named {0}'.format(interim_file_1PathName))


def process_interim_file():
    try:
        with open(sanitizedFilePathName, "w") as sanitizedFile:
            print("processing interim file 2")
            with open(interim_file_2PathName, "r") as interim_file_2:
                currently_in_message = False
                current_message_string = ''
                total_sip_messages = 0
                for line in interim_file_2:
                    if currently_in_message:
                        if sanitized_message_separator_regex.match(line):
                            # some messages are two bytes too long, because of weirdness in our logging code!
                            # No real way to figure out which
                            # ones, except by instantiating a SIPMessage and checking.  Look for messages
                            # that are exactly two bytes too long, and chop them down.
                            sip_message = SIPMessageFactory().next_for_string(current_message_string)
                            truncate_bytes = sip_message.content.__len__() - sip_message.header.content_length
                            if truncate_bytes == 2:
                                current_message_string = current_message_string[:current_message_string.__len__() - 2]

                            sanitizedFile.write(current_message_string)
                            sanitizedFile.write(line)
                            currently_in_message = False
                        else:
                            current_message_string += line
                    else:
                        if any(regex.match(line) for regex in start_line_regexes):
                            # print "."
                            total_sip_messages += 1
                            currently_in_message = True
                            current_message_string = ''
                            sanitizedFile.write(line)
                print(str(total_sip_messages) + " total SIP messages")
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


def delete_interim_files():
    try:
        os.remove(interim_file_1PathName)
        os.remove(interim_file_2PathName)
    except OSError:
        pass


# @profile
def process_pcap_files():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing pcap files")
            for pcapDirectoryPathName in pcapDirectoryPathNames:
                for pcapFilePathName in sorted(glob.iglob(pcapDirectoryPathName + '/*.pcap')):
                    print(pcapFilePathName)
                    with open(pcapFilePathName, "r") as pcapFile:
                        for ts, pkt in dpkt.pcap.Reader(pcapFile):
                            eth = dpkt.ethernet.Ethernet(pkt)
                            if eth.type != dpkt.ethernet.ETH_TYPE_IP:
                                continue
                            ip = eth.data
                            if (ip.p == dpkt.ip.IP_PROTO_UDP or ip.p == dpkt.ip.IP_PROTO_TCP) and ip.data.dport in [5060, 5062, 5080]:
                                data = ip.data.data
                                if data.__len__() > 2:
                                    if re.match('[^\s]+', data):  # Bria and some others periodically send CRLFCRLF by itself, presumably as a keepalive.  We don't want those.
                                        sanitizedFile.write(data)
                                        sanitizedFile.write(message_separator + "\r\n")
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


# @profile
def process_freeswitch_files():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing Freeswitch files")
            for freeswitchDirectoryPathName in freeswitchDirectoryPathNames:
                for freeswitchFilePathName in sorted(glob.iglob(freeswitchDirectoryPathName + '/*')):
                    print(freeswitchFilePathName)
                    with open(freeswitchFilePathName, "r") as freeswitchFile:
                        stringio = StringIO()
                        state = 'outsideOfMessage'
                        line_number = 0
                        for line in freeswitchFile:
                            line_number += 1
                            if state == 'outsideOfMessage':
                                if re.match('^send \d+ bytes to', line) or re.match('^recv \d+ bytes from', line):
                                    state = 'waitingForFirstDashes'
                            elif state == 'waitingForFirstDashes':
                                if re.match('^   ---------------', line):
                                    stringio = StringIO()
                                    state = 'inMessage'
                                else:
                                    print('ERROR!  Line {0} - First dashes not found.'.format(line_number))
                                    stringio.close()
                                    state = 'outsideOfMessage'
                            elif state == 'inMessage':
                                if re.match('^   ---------------', line):
                                    sanitizedFile.write(stringio.getvalue())
                                    sanitizedFile.write(message_separator + "\r\n")
                                    stringio.close()
                                    state = 'outsideOfMessage'
                                else:
                                    if not re.match('^   ', line):
                                        print('WARNING!  Line {0} - In message, but line is not preceeded by 3 spaces.  Rejecting message.'.format(line_number))
                                        stringio.close()
                                        state = 'outsideOfMessage'
                                    else:
                                        stringio.write(line[3:].replace('\n', '\r\n'))
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


# @profile
def process_kamailio_files():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing Kamailio files")
            for kamailioDirectoryPathName in kamailioDirectoryPathNames:
                for kamailioFilePathName in sorted(glob.iglob(kamailioDirectoryPathName + '/*')):
                    print(kamailioFilePathName)
                    with open(kamailioFilePathName, "r") as kamailioFile:
                        # TODO
                        pass
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


# @profile
def process_nec_3c_files():
    try:
        with open(sanitizedFilePathName, "a") as sanitizedFile:
            print("processing NEC 3C files")
            for nec3cDirectoryPathName in nec3cDirectoryPathNames:
                for nec3cFilePathName in sorted(glob.iglob(nec3cDirectoryPathName + '/*')):
                    print(nec3cFilePathName)
                    with open(nec3cFilePathName, "r") as nec3cFile:
                        # TODO
                        pass
    except IOError:
        print('WARNING:  could not create sanitized file named {0}'.format(sanitizedFilePathName))


def run_all():
    create_interim_1_file()
    create_interim_2_file()
    process_interim_file()
    delete_interim_files()
    process_pcap_files()
    process_freeswitch_files()
    process_kamailio_files()
    process_nec_3c_files()

if __name__ == '__main__':
    for logFileDict in bobstack.tests_slow.testlogfilelocations.logFileDicts:
        # raw_log_file_directory_path_names = [ '../proprietary-test-data/big-lab-test-logs-raw',
        #                                  '../proprietary-test-data/cust-1-logs-raw',
        #                                  '../proprietary-test-data/cust-3-logs-raw' ]

        # raw_log_file_directory_path_names = []
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cloud',
        #                            '../proprietary-test-data/big-lab-test-logs-pcap',
        #                            '../proprietary-test-data/client-lab-test-logs-pcap',
        #                            '../proprietary-test-data/cust-2-logs-pcap',
        #                            '../proprietary-test-data/cust-4-logs-pcap',
        #                            '../proprietary-test-data/from-bobstack-testbed' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cloud' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/cust-2-logs-pcap' ]
        # pcapDirectoryPathNames = [ '../proprietary-test-data/from-bobstack-testbed' ]
        raw_log_file_directory_path_names = logFileDict['rawLogFileDirectoryPathNames']
        pcapDirectoryPathNames = logFileDict['pcapDirectoryPathNames']
        freeswitchDirectoryPathNames = logFileDict['freeswitchDirectoryPathNames']
        kamailioDirectoryPathNames = logFileDict['kamailioLogFileDirectoryPathNames']
        nec3cDirectoryPathNames = logFileDict['nec3cLogFileDirectoryPathNames']
        interim_file_1PathName = logFileDict['interimFile1PathName']
        interim_file_2PathName = logFileDict['interimFile2PathName']
        sanitizedFilePathName = logFileDict['sanitizedFilePathName']

        # print timeit.timeit(create_interim_1_file, number=1)
        # print timeit.timeit(create_interim_2_file, number=1)
        # print timeit.timeit(process_interim_file, number=1)
        # delete_interim_files()
        # print timeit.timeit(process_pcap_files, number=1)
        print(timeit.timeit(run_all, number=1))
