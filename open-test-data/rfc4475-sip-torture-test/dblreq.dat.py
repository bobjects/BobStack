        messageString = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:j.user@example.com\r\n'
            'From: sip:j.user@example.com;tag=43251j3j324\r\n'
            'Max-Forwards: 8\r\n'
            'I: dblreq.0ha0isndaksdj99sdfafnl3lk233412\r\n'
            'Contact: sip:j.user@host.example.com\r\n'
            'CSeq: 8 REGISTER\r\n'
            'Via: SIP/2.0/UDP 192.0.2.125;branch=z9hG4bKkdjuw23492\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
            '\r\n'
            'INVITE sip:joe@example.com SIP/2.0\r\n'
            't: sip:joe@example.com\r\n'
            'From: sip:caller@example.net;tag=141334\r\n'
            'Max-Forwards: 8\r\n'
            'Call-ID: dblreq.0ha0isnda977644900765@192.0.2.15\r\n'
            'CSeq: 8 INVITE\r\n'
            'Via: SIP/2.0/UDP 192.0.2.15;branch=z9hG4bKkdjuw380234\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.15\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.15\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm =video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
            '\r\n'
        )
