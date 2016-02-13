# Only RFC2361 headers so far.  Not yet processing these:
# Accept-Resource-Priority
# Av-Global-Session-ID
# Alert-Info
# Allow-Events
# Cisco-Guid
# Event
# History-Info
# Min-SE
# P-Asserted-Identity
# P-Called-Party-Id
# P-Preferred-Identity
# P-RTP-Stat
# Privacy
# Reason
# Record-Session-Expires
# Refer-To
# Referred-By
# Remote-Party-ID
# Remote-Party-Id
# Replaces
# Resource-Priority
# Subscription-State
# X-RTP-Stat
# x-channel
# x-nt-alter-id
# x-nt-corr-id
# x-nt-guid
# x-nt-location
# x-nt-party-id
# x-nt-resource-priority

rm testForAllFactory.py

for HYPHENATED in Accept Accept-Encoding Accept-Language Allow Authorization CSeq Call-ID Call-Info Contact Content-Disposition Content-Type Date Expires From Max-Forwards Record-Route Require Retry-After Route Server Session-Expires Supported Timestamp To User-Agent Via WWW-Authenticate Warning
do
	NONHYPHENATED=`echo "$HYPHENATED" | sed  -e s/-//g`
	CLASS=$NONHYPHENATED"SIPHeaderField"
	FILENAMESTART=`echo "$NONHYPHENATED" | perl -ne 'print lcfirst'`
	UPPERCASE=`echo "$HYPHENATED" | perl -ne 'print uc'`
	LOWERCASE=`echo "$HYPHENATED" | perl -ne 'print lc'`
	FILENAMEENDING=SIPHeaderField.py
	TARGETFILENAME=testForFactory$CLASS.py
	cp testForFactoryFooBar.py $TARGETFILENAME
	# Farking OS X sed syntax.  Grrr...
	# sed -i $targetFilename -e s/OPTIONS/$method/g
	sed -i ''  -e s/Foo-Bar/$HYPHENATED/g $TARGETFILENAME
	sed -i ''  -e s/FooBar/$NONHYPHENATED/g $TARGETFILENAME
	sed -i ''  -e s/FOO-BAR/$UPPERCASE/g $TARGETFILENAME
	sed -i ''  -e s/foo-bar/$LOWERCASE/g $TARGETFILENAME
	cat $TARGETFILENAME >> testForAllFactory.py
done
