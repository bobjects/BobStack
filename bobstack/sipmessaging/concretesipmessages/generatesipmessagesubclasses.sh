for method in ACK BYE CANCEL INFO INVITE NOTIFY PRACK PUBLISH MESSAGE REFER REGISTER SUBSCRIBE UPDATE
do
	lowercase=`echo "$method" | perl -ne 'print lc'`
	# filenameEnding=SIPRequest.py
	filenameEnding=.py
	# targetFilename=$lowercase$filenameEnding
	targetFilename=foo$lowercase$filenameEnding
	echo processing $method $lowercase
	cp fooOPTIONS.py $targetFilename
	# Farking OS X sed syntax.  Grrr...
	# sed -i $targetFilename -e s/OPTIONS/$method/g
	sed -i ''  -e s/OPTIONS/$method/g $targetFilename
done
