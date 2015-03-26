#!usr/bin/perl
use strict;
use warnings;

my $line = "this\tis\ta\ttab\tdelimited\tline";
#my $line = "this is not a tab delimited line";
my @cols;

if($line =~ /\t/){
    @cols = split('\t', $line);
}else{
    print "This is not a tab-delimited line.\n";
}

foreach (@cols){
    print $_."\n";
}
