        messageString = (
            'INVITE sip:user@company.com SIP/2.0\r\n'
            'Contact: <sip:caller@host25.example.net>\r\n'
            'Via: SIP/2.0/UDP 192.0.2.25;branch=z9hG4bKkdjuw\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 5 INVITE\r\n'
            'Call-ID: multi01.98asdh@192.0.2.1\r\n'
            'CSeq: 59 INVITE\r\n'
            'Call-ID: multi01.98asdh@192.0.2.2\r\n'
            'From: sip:caller@example.com;tag=3413415\r\n'
            'To: sip:user@example.com\r\n'
            'To: sip:other@example.net\r\n'
            'From: sip:caller@example.net;tag=2923420123\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 154\r\n'
            'Contact: <sip:caller@host36.example.net>\r\n'
            'Max-Forwards: 5\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.25\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.25\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
            '\r\n'
        )