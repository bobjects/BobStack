        messageString = (
            'INVITE sip:user@[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@[2001:db8::10]\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::9:1];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::9:1]>\r\n'
            'Max-Forwards: 70\r\n'
            'CSeq: 8912 INVITE\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 181\r\n'
            '\r\n'
            'v=0\r\n'
            'o=bob 280744730 28977631 IN IP4 host.example.com\r\n'
            's=\r\n'
            't=0 0\r\n'
            'm=audio 22334 RTP/AVP 0\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            'm=video 6024 RTP/AVP 107\r\n'
            'c=IN IP6 2001:db8::1\r\n'
            'a=rtpmap:107 H263-1998/90000\r\n'
        )