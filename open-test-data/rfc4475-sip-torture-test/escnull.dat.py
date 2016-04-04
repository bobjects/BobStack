        messageString = (
            'REGISTER sip:example.com SIP/2.0\r\n'
            'To: sip:null-%00-null@example.com\r\n'
            'From: sip:null-%00-null@example.com;tag=839923423\r\n'
            'Max-Forwards: 70\r\n'
            'Call-ID: escnull.39203ndfvkjdasfkq3w4otrq0adsfdfnavd\r\n'
            'CSeq: 14398234 REGISTER\r\n'
            'Via: SIP/2.0/UDP host5.example.com;branch=z9hG4bKkdjuw\r\n'
            'Contact: <sip:%00@host5.example.com>\r\n'
            'Contact: <sip:%00%00@host5.example.com>\r\n'
            'L:0\r\n'
            '\r\n'
        )
