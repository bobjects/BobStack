import glob
import os
import re

directoryPaths = ['/Users/bob/bobstack/open-test-data/rfc4475-sip-torture-test', '/Users/bob/bobstack/open-test-data/rfc5118-sip-torture-test']
for directoryPath in directoryPaths:
    print directoryPath
    for datFilePathName in sorted(glob.iglob(directoryPath + '/*.dat')):
        print '    ' + datFilePathName
        pyFilePathName = datFilePathName + ".py"
        with open(datFilePathName, "r") as datFile:
            with open(pyFilePathName, "w") as pyFile:
                pyFile.write("        messageString = (\r\n")
                for line in datFile:
                    pyFile.write("            '")
                    pyFile.write(line.rstrip('\r\n'))
                    pyFile.write("\\r\\n'\r\n")
                pyFile.write("        )\r\n")
