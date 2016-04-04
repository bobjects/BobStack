        messageString = (
            'OPTIONS sip:user@example.com SIP/2.0\r\n'
            'To: sip:j_user@example.com\r\n'
            'From: sip:caller@example.net;tag=242etr\r\n'
            'Max-Forwards: 6\r\n'
            'Call-ID: bext01.0ha0isndaksdj\r\n'
            'Require: nothingSupportsThis, nothingSupportsThisEither\r\n'
            'Proxy-Require: noProxiesSupportThis, norDoAnyProxiesSupportThis\r\n'
            'CSeq: 8 OPTIONS\r\n'
            'Via: SIP/2.0/TLS fold-and-staple.example.com;branch=z9hG4bKkdjuw\r\n'
            'Content-Length: 0\r\n'
            '\r\n'
        )
