import os
import re
import timeit

import dpkt

counter=0
ipcounter=0
tcpcounter=0
udpcounter=0

# filename='../open-test-data/from-wireshark-site/aaa.pcap'
filename='../proprietary-test-data/cloud-resaved/2016.02.14.001.pcap'
with open(filename, "r") as f:
    for ts, pkt in dpkt.pcap.Reader(f):

        counter+=1
        eth=dpkt.ethernet.Ethernet(pkt)
        if eth.type!=dpkt.ethernet.ETH_TYPE_IP:
           continue

        # print eth
        # print "**** DATA ****"
        ip=eth.data
        # ipcounter+=1
        #
        # if ip.p==dpkt.ip.IP_PROTO_TCP:
        #    tcpcounter+=1

        if ip.p==dpkt.ip.IP_PROTO_UDP and ip.data.dport == 5060:
            print "**** ip ****"
            print ip
            data = ip.data.data
            print data
            # sip = dpkt.sip.Request(ip.data)
            # print "**** sip ****"
            # print sip
            print dpkt.sip.Request(ip.data.data)
            print "**** ip.data.data ****"
            print str(ip.data.data)


"""
from pprint import pprint
from pcapfile import savefile


filename='../proprietary-test-data/cloud-resaved/2016.02.14.001.pcap'
filename='../open-test-data/from-wireshark-site/aaa.pcap'
with open(filename, "r") as f:
    capfile = savefile.load_savefile(f, layers=3, verbose=True)
    # print capfile
    pkt = capfile.packets[19]
    pprint(dir(pkt))
    pprint(dir(pkt.packet))
    # print pkt.raw()
    # print pkt.timestamp
    # print pkt.packet
    print pkt.packet.src
    print pkt.packet.dst
    print pkt.packet.type
    # print pkt.raw()
    print pkt.packet.payload.__class__
    pprint(dir(pkt.packet.payload))
    print pkt.packet.payload
    print pkt.packet.payload.off
    print pkt.packet.payload.pad
    print pkt.packet.payload.payload.decode("hex")
    payload = pkt.packet.payload.payload.decode("hex")
    print "done"
    # print pkt.header
    # print pkt.capture_len
"""