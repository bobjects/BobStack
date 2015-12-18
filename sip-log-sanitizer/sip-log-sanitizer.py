#!/usr/bin/python
import os
import sys
import re

# interimFile1PathName = '/tmp/interim1.txt'
# interimFile2PathName = '/tmp/interim2.txt'
interimFile1PathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-sanitized/interim1.txt'
interimFile2PathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-sanitized/interim2.txt'
rawLogFileDirectoryPathName = '/Users/bob/bobstack/proprietary-test-data/ft-huachuca-test-logs-raw'
interimFile1 = None
interimFile2 = None
rawLogFile = None

interimFile1 = open(interimFile1PathName, "w")
for rawLogFilePathName in os.listdir(rawLogFileDirectoryPathName):
    print rawLogFilePathName
    rawLogFile = open(rawLogFileDirectoryPathName + "/" + rawLogFilePathName, "r")
    for line in rawLogFile:
        line = line.replace("\r\r\n", "\r\n")
        if re.search("^>>>>>>>>>>  [^>]*>>>>>>>>>>>", line):
            #print "."
            line = "\r\n"
            pass
        # if re.search("^>>>>>>>>>>  [^\s]*  >>>>>>>>>>$", line):
        if re.search("^>>>>>>>>>>  [^>]*>>>>>>>>>>", line):
            #print "."
            line = "\r\n"
            pass
        # if re.search("^<<<<<<<<<<\s\s[^\s]*\s\s<<<<<<<<<<", line):
        if re.search("^<<<<<<<<<<  [^>]*<<<<<<<<<<", line):
        #  '^Resource-Priority:\s+([^-]+)-(\d+)\.(\d)' ) search: 'Resource-Priority: uc-000000.2'
            #print "."
            line = "\r\n"
            pass
        if re.search("^\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\* [^\*]*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*", line):
            #print "."
            line = "\r\n"
            pass
        if re.search("^##################################### [^#]*##########################", line):
            #print "."
            line = "\r\n"
            pass
        interimFile1.write(line)
        # interimFile1.write("\r\n")
    rawLogFile.close()
    interimFile1.write("\r\n")
interimFile1.close()


