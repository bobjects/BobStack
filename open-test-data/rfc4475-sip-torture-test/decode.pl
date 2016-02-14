#!/usr/bin/perl
   use strict;
   my $bdata = "";
   use MIME::Base64;
   while(<>) {
     if (/-- BEGIN MESSAGE ARCHIVE --/ .. /-- END MESSAGE ARCHIVE --/) {
          if ( m/^\s*[^\s]+\s*$/) {
              $bdata = $bdata . $_;
          }
     }
   }
   print decode_base64($bdata);

