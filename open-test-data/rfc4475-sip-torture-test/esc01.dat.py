        messageString = (
            'INVITE sip:sips%3Auser%40example.com@example.net SIP/2.0\r\n'
            'To: sip:%75se%72@example.com\r\n'
            'From: <sip:I%20have%20spaces@example.net>;tag=938\r\n'
            'Max-Forwards: 87\r\n'
            'i: esc01.239409asdfakjkn23onasd0-3234\r\n'
            'CSeq: 234234 INVITE\r\n'
            'Via: SIP/2.0/UDP host5.example.net;branch=z9hG4bKkdjuw\r\n'
            'C: application/sdp\r\n'
            'Contact:\r\n'
            '  <sip:cal%6Cer@host5.example.net;%6C%72;n%61me=v%61lue%25%34%31>\r\n'
            'Content-Length: 150\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.1\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.1\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
