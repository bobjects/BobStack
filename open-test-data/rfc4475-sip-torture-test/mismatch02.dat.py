        messageString = (
            'NEWMETHOD sip:user@example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:caller@example.net;tag=34525\r\n'
            'Max-Forwards: 6\r\n'
            'Call-ID: mismatch02.dj0234sxdfl3\r\n'
            'CSeq: 8 INVITE\r\n'
            'Contact: <sip:caller@host.example.net>\r\n'
            'Via: SIP/2.0/UDP host.example.net;branch=z9hG4bKkdjuw\r\n'
            'Content-Type: application/sdp\r\n'
            'l: 138\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
