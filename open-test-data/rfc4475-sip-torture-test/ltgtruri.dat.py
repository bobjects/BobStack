        messageString = (
            'INVITE <sip:user@example.com> SIP/2.0\r\n'
            'To: sip:user@example.com\r\n'
            'From: sip:caller@example.net;tag=39291\r\n'
            'Max-Forwards: 23\r\n'
            'Call-ID: ltgtruri.1@192.0.2.5\r\n'
            'CSeq: 1 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.5\r\n'
            'Contact: <sip:caller@host5.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 159\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.5\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.5\r\n'
            't=3149328700 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
