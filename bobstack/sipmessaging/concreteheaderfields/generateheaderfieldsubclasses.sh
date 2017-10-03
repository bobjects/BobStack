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

	# echo "        elif $CLASS.can_match_string(a_string):"
	# echo "            return $CLASS.new_parsed_from(a_string)"

	# echo "        elif $CLASS.can_match_field_name(a_string):"
	# echo "            return $CLASS.new_for_field_name_and_value_string(field_name=a_string)"

	# echo "        elif $CLASS.can_match_field_name(field_name):"
	# echo "            return $CLASS.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)"

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
        # echo "            header_field = self.sipHeaderFieldClassUnderTest.new_parsed_from(line)" >> out
        # echo "            self.assertTrue(header_field.is$NONHYPHENATED, line)" >> out
        # echo "" >> out
        # echo "    def test_rendering(self):" >> out
        # echo "        self.basic_test_rendering()" >> out
        # echo "        for field_name in self.canonicalFieldNames:" >> out
        # echo "            for field_value_string in self.canonicalFieldValues:" >> out
        # echo "                header_field = self.sipHeaderFieldClassUnderTest.new_for_field_name_and_value_string(field_name=field_name, field_value_string=field_value_string)" >> out
        # echo "                self.assertTrue(header_field.is$NONHYPHENATED)" >> out
        # echo "                header_field = self.sipHeaderFieldClassUnderTest.new_for_value_string(field_value_string=field_value_string)" >> out
        # echo "                self.assertTrue(header_field.is$NONHYPHENATED)" >> out
        # echo "                header_field = self.sipHeaderFieldClassUnderTest.new_for_attributes(field_value_string=field_value_string)" >> out
        # echo "                self.assertTrue(header_field.is$NONHYPHENATED)" >> out
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
        # echo "            header_field = SIPHeaderFieldFactory().next_for_string(line)" >> out
        # echo "            self.assertTrue(header_field.is$NONHYPHENATED, line)" >> out
        # echo "            stringio = StringIO(line + '\r\n')" >> out
        # echo "            header_field = SIPHeaderFieldFactory().all_for_stringio(stringio)[0]" >> out
        # echo "            self.assertTrue(header_field.is$NONHYPHENATED, line)" >> out
        # echo "            stringio.close()" >> out
        # echo "            header_field = SIPHeaderFieldFactory().next_for_field_name(self.canonicalFieldNames[0])" >> out
        # echo "            self.assertTrue(header_field.is$NONHYPHENATED, line)" >> out
        # echo '            header_field = SIPHeaderFieldFactory().next_for_field_name_and_field_value(self.canonicalFieldNames[0], "foo bar baz blarg")' >> out
        # echo "            self.assertTrue(header_field.is$NONHYPHENATED, line)" >> out
        # echo "" >> out
        # echo "" >> out

       echo "            if header_field.is$NONHYPHENATED:" >> out
       echo "                self.appendStringToFileNamed(header_field.raw_string + '\r\n', '$TARGETFILENAMESANSEXTENSION')" >> out


done
