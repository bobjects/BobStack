        messageString = (
            'INVITE sip:user@example.com SIP/2.0\r\n'
            'Max-Forwards: 254\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=32394234\r\n'
            'Call-ID: ncl.0ha0isndaksdj2193423r542w35\r\n'
            'CSeq: 0 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.53;branch=z9hG4bKkdjuw\r\n'
            'Contact: <sip:caller@example53.example.net>\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: -999\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.53\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.53\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
