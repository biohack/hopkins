#!/usr/bin/perl -w
use strict;
use warnings;
use CGI ();
my $cgi = CGI->new;
print $cgi->header;
my $string = $cgi -> param("myString");
=d
my $database = $cgi->param("database");
my $accession = $cgi->param("accession");
my $description = $cgi->param("description");
my $score = $cgi->param("score");
my $evalue = $cgi->param("evalue");
my $string = $database."\t".$accession."\t".$description."\t".$score."\t".$evalue."\n";
=cut
open (FILE, ">", "/var/www/shwang26/final/refine.txt") || die "Could not open: $!";
print FILE $string;
close FILE;
