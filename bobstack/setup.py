#!/usr/bin/env python
from distutils.core import setup
setup(name = 'bobstack',
      description = 'BobStack real time media platform',
      # long_description = ''
      version = '20160213',
      packages = ['sipmessaging', 'sipmessaging.concreteheaderfields', 'sipmessaging.concretesipmessages', 'tests'],
      data_files = [('', ['prepare-centos-6-cpython.sh', 'run-all-unit-tests.sh'])],

      test_suite = 'tests',
      # meta-data for upload to PyPi
      author = "Bobjects Incorporated",
      author_email = "bob@bobjectsinc.com",
      license = "Apache",
      url = "https://bobjectsinc.com",
      # download_url = ''
      keywords = "BobStack SIP WebRTC RTP VoIP telephony RFC3261",
      )

