        messageString = (
            'INVITE sip:vivekg@chair-dnrc.example.com;unknownparam SIP/2.0\r\n'
            'TO :\r\n'
            ' sip:vivekg@chair-dnrc.example.com ;   tag    = 1918181833n\r\n'
            'from   : "J Rosenberg \\\""       <sip:jdrosen@example.com>\r\n'
            '  ;\r\n'
            '  tag = 98asjd8\r\n'
            'MaX-fOrWaRdS: 0068\r\n'
            'Call-ID: wsinv.ndaksdj@192.0.2.1\r\n'
            'Content-Length   : 150\r\n'
            'cseq: 0009\r\n'
            '  INVITE\r\n'
            'Via  : SIP  /   2.0\r\n'
            ' /UDP\r\n'
            '    192.0.2.2;branch=390skdjuw\r\n'
            's :\r\n'
            'NewFangledHeader:   newfangled value\r\n'
            ' continued newfangled value\r\n'
            'UnknownHeaderWithUnusualValue: ;;,,;;,;\r\n'
            'Content-Type: application/sdp\r\n'
            'Route:\r\n'
            ' <sip:services.example.com;lr;unknownwith=value;unknown-no-value>\r\n'
            'v:  SIP  / 2.0  / TCP     spindle.example.com   ;\r\n'
            '  branch  =   z9hG4bK9ikj8  ,\r\n'
            ' SIP  /    2.0   / UDP  192.168.255.111   ; branch=\r\n'
            ' z9hG4bK30239\r\n'
            'm:"Quoted string \"\"" <sip:jdrosen@example.com> ; newparam =\r\n'
            '      newvalue ;\r\n'
            '  secondparam ; q = 0.33\r\n'
            '\r\n'
            'v=0\r\n'
            'o=mhandley 29739 7272939 IN IP4 192.0.2.3\r\n'
            's=-\r\n'
            'c=IN IP4 192.0.2.4\r\n'
            't=0 0\r\n'
            'm=audio 49217 RTP/AVP 0 12\r\n'
            'm=video 3227 RTP/AVP 31\r\n'
            'a=rtpmap:31 LPC\r\n'
        )
