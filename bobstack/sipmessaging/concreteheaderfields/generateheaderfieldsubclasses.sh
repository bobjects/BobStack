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

for HYPHENATED in Accept Accept-Encoding Accept-Language Allow Authorization CSeq Call-ID Call-Info Contact Content-Disposition Content-Type Date Expires From Max-Forwards Record-Route Require Retry-After Route Server Session-Expires Supported Timestamp To User-Agent WWW-Authenticate Warning
do
	# echo $HYPHENATED
	NONHYPHENATED=`echo "$HYPHENATED" | sed  -e s/-//g`
	CLASS=$NONHYPHENATED"SIPHeaderField"
	# echo $NONHYPHENATED
	FILENAMESTART=`echo "$NONHYPHENATED" | perl -ne 'print lcfirst'`
	FILENAMEENDING=SIPHeaderField.py
	TARGETFILENAME=$FILENAMESTART$FILENAMEENDING
	TARGETFILENAMESANSEXTENSION=`echo "$TARGETFILENAME" | sed  -e s/\.py//g`
	# echo $TARGETFILENAME
	# echo processing $TARGETFILENAME
	cp fooBarSIPHeaderField.py $TARGETFILENAME
	# Farking OS X sed syntax.  Grrr...
	# sed -i $targetFilename -e s/OPTIONS/$method/g
	sed -i ''  -e s/Foo-Bar/$HYPHENATED/g $TARGETFILENAME
	sed -i ''  -e s/FooBar/$NONHYPHENATED/g $TARGETFILENAME
	# echo from $TARGETFILENAMESANSEXTENSION import $NONHYPHENATED"SIPHeaderField"
	# echo from concreteheaderfields import $NONHYPHENATED"SIPHeaderField"
	# echo from sipmessaging import $NONHYPHENATED"SIPHeaderField"

	# echo "        elif $CLASS.canMatchString(aString):"
	# echo "            return $CLASS.newParsedFrom(aString)"

	# echo "        elif $CLASS.canMatchFieldName(aString):"
	# echo "            return $CLASS.newForFieldNameAndValueString(fieldName=aString)"

	# echo "        elif $CLASS.canMatchFieldName(fieldName):"
	# echo "            return $CLASS.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)"

	echo "    @property"
	echo "    def is$CLASS(self):"
	echo "        return False"
	echo ""
done
