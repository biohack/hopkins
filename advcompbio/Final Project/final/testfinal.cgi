#!/usr/bin/env perl
use strict;
use warnings;
use Bio::Tools::Run::RemoteBlast;
use CGI ':standard';
use finalpackage('parse');
use JSON;
STDOUT->autoflush(1);

#create our CGI and TMPL objects
my $cgi = new CGI;
my $json = JSON->new->allow_nonref;

###JSON-HTML
#my $query = $cgi-> param('search_term');

###TESTING
print "Please enter in sequence: ";
my $query = <STDIN>;

chomp($query);

my $db ='';
if($query =~ /^[AGCT]+$/i){
    $db = 'blastn';
}elsif($query =~ /^[GAVLIMFWPSTCYNQDEKRH]+$/i){
    $db = 'blastp';
}else{
#    print "Not a valid sequence!\n";
    exit;
}

open (FILE, '>input.fasta');
print FILE ">zinput_fasta\n".$query."\n";
close FILE;

#print p("START");

my $factory = Bio::Tools::Run::RemoteBlast->new( -prog       => 'blastn'   ,
                                                 -data       => 'nr'       ,
                                                 -expect     => '1e-3'    ,
                                                 -readmethod => 'SearchIO' );

my $str = Bio::SeqIO->new( -file    => 'input.fasta' ,
                           -format  => 'fasta'   );

#print "submitting BLASTs\n";
while( my $seq = $str->next_seq() ) {
    $factory->submit_blast( $seq );
    print '.';
    sleep 5;
}
#print "BLAST search done.\n";
#print "Polling for results";
while( my @rids = $factory->each_rid ) {
    foreach my $rid ( @rids ) {
	my $result = $factory->retrieve_blast( $rid );
	if( ref( $result )) {
	    my $output   = $result->next_result();
	    my $filename = $output->query_name().".testfinalout";
	    $factory->save_output( $filename );
	    $factory->remove_rid( $rid );
#	    print "\n\tGot ",$output->query_name(),"\n";
	}elsif( $result < 0 ) {
	    # some error occurred
	    $factory->remove_rid( $rid );
	}else {
	    print '.';
	    sleep 5;
	}
    }
}
#print "Done.\n";
my($first, $second, $third, $fourth, $fifth) = parse();
my @db = @$first;
my @acc = @$second;
my @desc = @$third;
my @score = @$fourth;
my @evalue = @$fifth;
my $count = scalar(@db);

#array_ref to store hash refs href
my $matches=[];

for(my $i=0; $i < scalar(@db); $i++){
    #hash ref:  $href->{ $key } = $value; 
    my $href = {};
    $href->{'database'}=$db[$i];
    $href->{'accession'}=$acc[$i];
    $href->{'description'}=$desc[$i];
    $href->{'score'}=$score[$i];
    $href->{'evalue'}=$evalue[$i];
#    while( my ($k, $v) = each %$href ) {
#        print "key: $k, value: $v.\n";
#    }
    push(@$matches, $href);
}
foreach(@$matches){
#    print $_."\n";
}

#print p("DONE");

print $cgi->header('application/json');

print $json->encode(
    { match_count => $count, matches => $matches }
    );
