        messageString = (
            'INVITE sip:user@[2001:db8::10] SIP/2.0\r\n'
            'To: sip:user@[2001:db8::10]\r\n'
            'From: sip:user@example.com;tag=81x2\r\n'
            'Via: SIP/2.0/UDP [2001:db8::20];branch=z9hG4bKas3-111\r\n'
            'Call-ID: SSG9559905523997077@hlau_4100\r\n'
            'Contact: "Caller" <sip:caller@[2001:db8::20]>\r\n'
            'CSeq: 8612 INVITE\r\n'
            'Max-Forwards: 70\r\n'
            'Content-Type: application/sdp\r\n'
            'Content-Length: 268\r\n'
            '\r\n'
            'v=0\r\n'
            'o=assistant 971731711378798081 0 IN IP6 2001:db8::20\r\n'
            's=Live video feed for today's meeting\r\n'
            'c=IN IP6 2001:db8::20\r\n'
            't=3338481189 3370017201\r\n'
            'm=audio 6000 RTP/AVP 2\r\n'
            'a=rtpmap:2 G726-32/8000\r\n'
            'm=video 6024 RTP/AVP 107\r\n'
            'a=rtpmap:107 H263-1998/90000\r\n'
        )
