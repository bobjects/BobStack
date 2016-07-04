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

rm out

# for HYPHENATED in Accept Accept-Encoding Accept-Language Allow Authorization CSeq Call-ID Call-Info Contact Content-Disposition Content-Type Date Expires From Max-Forwards Record-Route Require Retry-After Route Server Session-Expires Supported Timestamp To User-Agent WWW-Authenticate Warning
for HYPHENATED in Subject Referred-By Refer-To Allow-Events Event Content-Encoding RAck P-Charge Reply-To Unsupported P-Asserted-Identity P-Preferred-Identity Remote-Party-ID Alert-Info History-Info P-Called-Party-Id P-RTP-Stat Privacy Proxy-Authenticate Proxy-Authorization Proxy-Require Reason Record-Session-Expires Replaces Subscription-State Min-Expires
do
	# echo $HYPHENATED
	NONHYPHENATED=`echo "$HYPHENATED" | sed  -e s/-//g`
	LOWERCASE=`echo "$HYPHENATED" | tr "[:upper:]" "[:lower:]"`
	UPPERCASE=`echo "$HYPHENATED" | tr "[:lower:]" "[:upper:]"`
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
	
	# echo from $TARGETFILENAMESANSEXTENSION import $NONHYPHENATED"SIPHeaderField" >> out
	# echo from concreteheaderfields import $NONHYPHENATED"SIPHeaderField" >> out
	# echo from sipmessaging import $NONHYPHENATED"SIPHeaderField" >> out

	# echo "        elif $CLASS.canMatchString(aString):"
	# echo "            return $CLASS.newParsedFrom(aString)"

	# echo "        elif $CLASS.canMatchFieldName(aString):"
	# echo "            return $CLASS.newForFieldNameAndValueString(fieldName=aString)"

	# echo "        elif $CLASS.canMatchFieldName(fieldName):"
	# echo "            return $CLASS.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)"

	# echo "    @property" >> out
	# echo "    def is$CLASS(self):" >> out
	# echo "        return False" >> out
	# echo "" >> out

	# echo "sipmessaging/concreteheaderfields/$TARGETFILENAME" >> out

	# echo "        '$LOWERCASE': $CLASS," >> out
	# echo "        '$LOWERCASE:': $CLASS," >> out

	# echo "class Test$CLASS(AbstractSIPHeaderFieldTestCase):" >> out
        # echo "    @property" >> out
        # echo "    def canonicalFieldNames(self):" >> out
        # echo "        return['$HYPHENATED', '$UPPERCASE', '$LOWERCASE']" >> out
        # echo "" >> out
        # echo "    @property" >> out
        # echo "    def sipHeaderFieldClassUnderTest(self):" >> out
        # echo "        return $CLASS" >> out
        # echo "" >> out
        # echo "    def test_parsing(self):" >> out
        # echo "        self.basic_test_parsing()" >> out
        # echo "        for line in self.canonicalStrings:" >> out
        # echo "            headerField = self.sipHeaderFieldClassUnderTest.newParsedFrom(line)" >> out
        # echo "            self.assertTrue(headerField.is$NONHYPHENATED, line)" >> out
        # echo "" >> out
        # echo "    def test_rendering(self):" >> out
        # echo "        self.basic_test_rendering()" >> out
        # echo "        for fieldName in self.canonicalFieldNames:" >> out
        # echo "            for fieldValueString in self.canonicalFieldValues:" >> out
        # echo "                headerField = self.sipHeaderFieldClassUnderTest.newForFieldNameAndValueString(fieldName=fieldName, fieldValueString=fieldValueString)" >> out
        # echo "                self.assertTrue(headerField.is$NONHYPHENATED)" >> out
        # echo "                headerField = self.sipHeaderFieldClassUnderTest.newForValueString(fieldValueString=fieldValueString)" >> out
        # echo "                self.assertTrue(headerField.is$NONHYPHENATED)" >> out
        # echo "                headerField = self.sipHeaderFieldClassUnderTest.newForAttributes(fieldValueString=fieldValueString)" >> out
        # echo "                self.assertTrue(headerField.is$NONHYPHENATED)" >> out
        # echo "" >> out
        # echo "" >> out

        # echo "class TestSIPHeaderFieldFactoryFor$NONHYPHENATED(AbstractSIPHeaderFieldFromFactoryTestCase):" >> out
        # echo "    @property" >> out
        # echo "    def canonicalFieldNames(self):" >> out
        # echo "        return['$HYPHENATED', '$UPPERCASE', '$LOWERCASE']" >> out
        # echo "" >> out
        # echo "    @property" >> out
        # echo "    def sipHeaderFieldClassUnderTest(self):" >> out
        # echo "        return $CLASS" >> out
        # echo "" >> out
        # echo "    def test_parsing(self):" >> out
        # echo "        self.basic_test_parsing()" >> out
        # echo "        for line in self.canonicalStrings:" >> out
        # echo "            headerField = SIPHeaderFieldFactory().nextForString(line)" >> out
        # echo "            self.assertTrue(headerField.is$NONHYPHENATED, line)" >> out
        # echo "            stringio = StringIO(line + '\r\n')" >> out
        # echo "            headerField = SIPHeaderFieldFactory().allForStringIO(stringio)[0]" >> out
        # echo "            self.assertTrue(headerField.is$NONHYPHENATED, line)" >> out
        # echo "            stringio.close()" >> out
        # echo "            headerField = SIPHeaderFieldFactory().nextForFieldName(self.canonicalFieldNames[0])" >> out
        # echo "            self.assertTrue(headerField.is$NONHYPHENATED, line)" >> out
        # echo '            headerField = SIPHeaderFieldFactory().nextForFieldNameAndFieldValue(self.canonicalFieldNames[0], "foo bar baz blarg")' >> out
        # echo "            self.assertTrue(headerField.is$NONHYPHENATED, line)" >> out
        # echo "" >> out
        # echo "" >> out

       echo "            if headerField.is$NONHYPHENATED:" >> out
       echo "                self.appendStringToFileNamed(headerField.rawString + '\r\n', '$TARGETFILENAMESANSEXTENSION')" >> out


done
