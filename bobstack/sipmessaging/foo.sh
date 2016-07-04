for method in ACK BYE CANCEL INFO INVITE NOTIFY PRACK PUBLISH MESSAGE OPTIONS REFER REGISTER SUBSCRIBE UPDATE
do
	lowercase=`echo "$method" | perl -ne 'print lc'`
	echo "        self.assertFalse(aSIPRequest.is$method""Request)"
	# echo "        self.assertIsInstance(aSIPMessage.is$method""Request, bool)"
	# echo "from sipmessaging import $method""SIPRequest"
done
echo ""
